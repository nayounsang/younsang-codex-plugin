#!/usr/bin/env node

import { createWriteStream } from 'node:fs';
import { mkdir } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import { basename, dirname, resolve } from 'node:path';
import { createServer } from 'node:http';
import { StringDecoder } from 'node:string_decoder';

const MAX_BODY_BYTES = 16 * 1024 * 1024;
const OTEL_CONFIG = [
  'otel.trace_exporter=none',
  'otel.metrics_exporter=none',
  'otel.log_user_prompt=false',
  'otel.log_agent_responses=false',
  'otel.log_guardian_assessments=false',
];

function usage() {
  console.error(
    'Usage: node collect-skill-invocations.mjs --target-skill <name> --run-id <id> --cwd <workspace> --timeout-ms <ms> --max-tokens <count> --exec-jsonl <file.jsonl> --output <file.jsonl> -- codex exec --json ...',
  );
  process.exit(2);
}

function parseArgs(argv) {
  const separator = argv.indexOf('--');
  if (separator < 0) usage();

  const options = {};
  for (let index = 0; index < separator; index += 1) {
    const key = argv[index];
    if (!['--target-skill', '--run-id', '--cwd', '--timeout-ms', '--max-tokens', '--exec-jsonl', '--output'].includes(key)) usage();
    const value = argv[index + 1];
    if (!value || value.startsWith('--')) usage();
    options[key.slice(2).replaceAll('-', '')] = value;
    index += 1;
  }

  const command = argv[separator + 1];
  const commandArgs = argv.slice(separator + 2);
  if (!options.targetskill || !options.runid || !options.cwd || !options.timeoutms || !options.maxtokens || !options.execjsonl || !options.output || !command) usage();
  const timeoutMs = Number(options.timeoutms);
  const maxTokens = Number(options.maxtokens);
  if (!Number.isSafeInteger(timeoutMs) || timeoutMs < 1 || timeoutMs > 2_147_483_647 || !Number.isSafeInteger(maxTokens) || maxTokens < 1) usage();
  if (basename(command).toLowerCase().replace(/\.(cmd|exe)$/u, '') !== 'codex') {
    console.error('The command after -- must be the Codex CLI executable.');
    process.exit(2);
  }

  return {
    targetSkill: options.targetskill,
    runId: options.runid,
    cwd: resolve(options.cwd),
    timeoutMs,
    maxTokens,
    execJsonlPath: resolve(options.execjsonl),
    outputPath: resolve(options.output),
    command,
    commandArgs,
  };
}

function anyValue(value) {
  if (!value || typeof value !== 'object') return value ?? '';
  if ('stringValue' in value) return value.stringValue;
  if ('intValue' in value) return value.intValue;
  if ('doubleValue' in value) return value.doubleValue;
  if ('boolValue' in value) return value.boolValue;
  if ('bytesValue' in value) return '[bytes]';
  if ('arrayValue' in value) return (value.arrayValue.values ?? []).map(anyValue);
  if ('kvlistValue' in value) {
    return Object.fromEntries(
      (value.kvlistValue.values ?? []).map(({ key, value: entry }) => [key, anyValue(entry)]),
    );
  }
  return '';
}

function attributesToObject(attributes = []) {
  return Object.fromEntries(
    attributes.map(({ key, value }) => [key, anyValue(value)]),
  );
}

function eventName(record, attributes) {
  return record.eventName ?? attributes['event.name'] ?? anyValue(record.body);
}

function collectTargetInvocations(payload, targetSkill, runId, writeRecord) {
  let recordCount = 0;
  let skillInvocationCount = 0;
  let targetInvocationCount = 0;

  for (const resource of payload.resourceLogs ?? []) {
    for (const scope of resource.scopeLogs ?? []) {
      for (const record of scope.logRecords ?? []) {
        recordCount += 1;
        const attributes = attributesToObject(record.attributes);
        if (eventName(record, attributes) !== 'codex.skill_invocation') continue;

        const saved = {
          run_id: runId,
          event: 'codex.skill_invocation',
          skill: attributes['skill.name'] ?? null,
          is_target_skill: attributes['skill.name'] === targetSkill,
          invocation_type: attributes['skill.invocation_type'] ?? null,
          conversation_id: attributes['conversation.id'] ?? null,
          turn_id: attributes['turn.id'] ?? null,
          skill_scope: attributes['skill.scope'] ?? null,
          plugin_id: attributes['skill.plugin_id'] ?? null,
          time_unix_nano: record.timeUnixNano ?? null,
          observed_time_unix_nano: record.observedTimeUnixNano ?? null,
        };
        writeRecord(saved);
        skillInvocationCount += 1;
        if (saved.is_target_skill) targetInvocationCount += 1;
      }
    }
  }

  return { recordCount, skillInvocationCount, targetInvocationCount };
}

const options = parseArgs(process.argv.slice(2));
const outputPath = options.outputPath;
const summaryPath = `${outputPath}.summary.json`;
await mkdir(dirname(outputPath), { recursive: true });
await mkdir(dirname(options.execJsonlPath), { recursive: true });

let output;
let summaryFile;
let execJsonl;
function waitForOpen(stream) {
  return new Promise((resolveOpen, rejectOpen) => {
    stream.once('open', resolveOpen);
    stream.once('error', rejectOpen);
  });
}

try {
  output = createWriteStream(outputPath, { flags: 'wx', encoding: 'utf8' });
  summaryFile = createWriteStream(summaryPath, { flags: 'wx', encoding: 'utf8' });
  execJsonl = createWriteStream(options.execJsonlPath, { flags: 'wx' });
  await Promise.all([waitForOpen(output), waitForOpen(summaryFile), waitForOpen(execJsonl)]);
} catch (error) {
  output?.destroy();
  summaryFile?.destroy();
  execJsonl?.destroy();
  console.error(`Cannot create telemetry output: ${error.message}`);
  process.exit(2);
}

let requestCount = 0;
let receivedRecordCount = 0;
let invocationCount = 0;
let targetInvocationCount = 0;
let rejectedRequestCount = 0;
let outputError;
output.on('error', (error) => { outputError = error; });
summaryFile.on('error', (error) => { outputError = error; });
execJsonl.on('error', (error) => { outputError = error; });

const server = createServer((request, response) => {
  if (request.method !== 'POST' || new URL(request.url, 'http://127.0.0.1').pathname !== '/v1/logs') {
    response.writeHead(404).end();
    return;
  }

  let size = 0;
  const chunks = [];
  request.on('data', (chunk) => {
    size += chunk.length;
    if (size > MAX_BODY_BYTES) {
      request.destroy();
      response.writeHead(413).end();
      return;
    }
    chunks.push(chunk);
  });

  request.on('end', () => {
    try {
      const payload = JSON.parse(Buffer.concat(chunks).toString('utf8'));
      if (!payload || !Array.isArray(payload.resourceLogs)) {
        throw new Error('Expected an OTLP/HTTP JSON logs payload.');
      }

      requestCount += 1;
      const counts = collectTargetInvocations(payload, options.targetSkill, options.runId, (record) => {
        output.write(`${JSON.stringify(record)}\n`);
      });
      receivedRecordCount += counts.recordCount;
      invocationCount += counts.skillInvocationCount;
      targetInvocationCount += counts.targetInvocationCount;
      response.writeHead(200, { 'content-type': 'application/json' }).end('{}');
    } catch (error) {
      rejectedRequestCount += 1;
      console.error(`Rejected OTLP logs payload: ${error.message}`);
      response.writeHead(400, { 'content-type': 'application/json' }).end('{}');
    }
  });
});

server.requestTimeout = 30_000;
server.headersTimeout = 10_000;

function closeServer() {
  return new Promise((resolveClose) => server.close(resolveClose));
}

function endStream(stream) {
  return new Promise((resolveEnd) => stream.end(resolveEnd));
}

let child;
let interrupted = false;
let budgetStopReason;
let tokenUsage = 0;
let tokenUsageEventCount = 0;
let outputBuffer = '';
const stdoutDecoder = new StringDecoder('utf8');
let forceKillTimer;
let timeoutTimer;
function requestBudgetStop(reason) {
  if (budgetStopReason || !child || child.exitCode !== null) return;
  budgetStopReason = reason;
  child.kill('SIGTERM');
  forceKillTimer = setTimeout(() => child.kill('SIGKILL'), 2_000);
  forceKillTimer.unref();
}
function observeExecutionLine(line) {
  try {
    const event = JSON.parse(line);
    if (event.type !== 'turn.completed') return;
    const inputTokens = event.usage?.input_tokens;
    const outputTokens = event.usage?.output_tokens;
    if (!Number.isSafeInteger(inputTokens) || !Number.isSafeInteger(outputTokens)) {
      requestBudgetStop('token_usage_unavailable');
      return;
    }
    tokenUsageEventCount += 1;
    tokenUsage += inputTokens + outputTokens;
    if (tokenUsage >= options.maxTokens) requestBudgetStop('token_budget_reached');
  } catch {
    // Ignore non-JSON stdout lines; --json output is parsed when it is valid.
  }
}

for (const signal of ['SIGINT', 'SIGTERM']) {
  process.once(signal, () => {
    interrupted = true;
    child?.kill(signal);
  });
}

try {
  await new Promise((resolveListen, rejectListen) => {
    server.once('error', rejectListen);
    server.listen(0, '127.0.0.1', resolveListen);
  });

  const { port } = server.address();
  const exporter = `otel.exporter={otlp-http={endpoint="http://127.0.0.1:${port}/v1/logs",protocol="json"}}`;
  const configArgs = [
    '-c', exporter,
    ...OTEL_CONFIG.flatMap((config) => ['-c', config]),
  ];

  const startedAt = Date.now();
  child = spawn(options.command, [...configArgs, ...options.commandArgs], {
    stdio: ['inherit', 'pipe', 'inherit'],
    env: process.env,
    cwd: options.cwd,
  });
  child.stdout.on('data', (chunk) => {
    if (!execJsonl.write(chunk)) {
      child.stdout.pause();
      execJsonl.once('drain', () => child.stdout.resume());
    }
    process.stdout.write(chunk);
    outputBuffer += stdoutDecoder.write(chunk);
    let newlineIndex;
    while ((newlineIndex = outputBuffer.indexOf('\n')) >= 0) {
      const line = outputBuffer.slice(0, newlineIndex);
      outputBuffer = outputBuffer.slice(newlineIndex + 1);
      observeExecutionLine(line);
    }
  });

  timeoutTimer = setTimeout(() => requestBudgetStop('timeout'), options.timeoutMs);

  const childExit = await new Promise((resolveExit, rejectSpawn) => {
    child.once('error', rejectSpawn);
    child.once('close', (code, signal) => resolveExit({ code, signal }));
  });
  clearTimeout(timeoutTimer);
  clearTimeout(forceKillTimer);
  outputBuffer += stdoutDecoder.end();
  if (outputBuffer.trim()) observeExecutionLine(outputBuffer);

  await closeServer();
  await endStream(output);
  await endStream(execJsonl);
  const summary = {
    run_id: options.runId,
    target_skill: options.targetSkill,
    codex_exit_code: childExit.code,
    codex_signal: childExit.signal,
    elapsed_ms: Date.now() - startedAt,
    timeout_ms: options.timeoutMs,
    stop_reason: budgetStopReason ?? null,
    token_budget: options.maxTokens,
    token_usage: tokenUsage,
    token_usage_event_count: tokenUsageEventCount,
    token_usage_available: tokenUsageEventCount > 0,
    otlp_request_count: requestCount,
    received_log_record_count: receivedRecordCount,
    rejected_request_count: rejectedRequestCount,
    skill_invocation_event_count: invocationCount,
    target_invocation_event_count: targetInvocationCount,
    target_invocation_observed: targetInvocationCount > 0,
    invocation_detection: 'best_effort',
    execution_jsonl_path: options.execJsonlPath,
    telemetry_status: rejectedRequestCount > 0
      ? 'invalid_payload'
      : receivedRecordCount > 0
        ? 'received'
        : 'unverified',
    interrupted,
  };
  await new Promise((resolveWrite, rejectWrite) => {
    summaryFile.once('error', rejectWrite);
    summaryFile.end(`${JSON.stringify(summary, null, 2)}\n`, resolveWrite);
  });

  if (outputError) throw outputError;
  if (budgetStopReason) process.exitCode = budgetStopReason === 'timeout' ? 124 : 125;
  else if (childExit.code !== 0 || interrupted) process.exitCode = childExit.code ?? 1;
} catch (error) {
  clearTimeout(timeoutTimer);
  clearTimeout(forceKillTimer);
  await closeServer().catch(() => {});
  await endStream(output).catch(() => {});
  await endStream(execJsonl).catch(() => {});
  await endStream(summaryFile).catch(() => {});
  console.error(`Skill invocation collection failed: ${error.message}`);
  process.exitCode = 1;
}
