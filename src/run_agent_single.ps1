# PowerShell script to run single knowledge point test
# PowerShell 脚本运行单知识点测试

$PY = "python"
$ENTRY = "agent.py"

# Default values
$API = "gpt-41"
$FOLDER_PREFIX = "TEST-single"
$KNOWLEDGE_POINT = "Circle area formula"

# Hyperparameters
$MAX_CODE_TOKEN_LENGTH = 10000
$MAX_FIX_BUG_TRIES = 10
$MAX_REGENERATE_TRIES = 10
$MAX_FEEDBACK_GEN_CODE_TRIES = 3
$MAX_MLLM_FIX_BUGS_TRIES = 3
$FEEDBACK_ROUNDS = 2

# Check if knowledge_point is provided
if ($args -match "--knowledge_point") {
    $KNOWLEDGE_POINT = ($args | Select-String -Pattern "--knowledge_point\s+(\S+)" | ForEach-Object { $_.Matches.Groups[1].Value })
}

Write-Host "Running single knowledge point test..." -ForegroundColor Cyan
Write-Host "Knowledge Point: $KNOWLEDGE_POINT" -ForegroundColor Yellow
Write-Host "API: $API" -ForegroundColor Yellow

# Build command
$cmd = @(
    $PY,
    $ENTRY,
    "--API", $API,
    "--folder_prefix", $FOLDER_PREFIX,
    "--no_feedback",
    "--no_assets",
    "--max_code_token_length", $MAX_CODE_TOKEN_LENGTH,
    "--max_fix_bug_tries", $MAX_FIX_BUG_TRIES,
    "--max_regenerate_tries", $MAX_REGENERATE_TRIES,
    "--max_feedback_gen_code_tries", $MAX_FEEDBACK_GEN_CODE_TRIES,
    "--max_mllm_fix_bugs_tries", $MAX_MLLM_FIX_BUGS_TRIES,
    "--feedback_rounds", $FEEDBACK_ROUNDS,
    "--knowledge_point", "`"$KNOWLEDGE_POINT`""
)

# Execute
& $cmd[0] $cmd[1..($cmd.Length-1)]
