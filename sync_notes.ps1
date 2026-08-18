# FastAPI 学习笔记自动同步脚本
# 功能：把 E 盘笔记复制到仓库 notes/ 目录，有变化则自动提交并推送 GitHub
$repo    = "D:\Python-Project\FASTAPI_CODE"
$noteDir = "E:\个人文件\笔记\conqyerdeny\python"

# 要同步的笔记文件（想加新的就往这里加一行）
$files = @(
    "fastAPI  笔记.md",
    "HTTP基础.md"
)

Set-Location $repo

$missed = @()
foreach ($f in $files) {
    $src = Join-Path $noteDir $f
    if (Test-Path -LiteralPath $src) {
        Copy-Item -LiteralPath $src -Destination (Join-Path $repo "notes\$f") -Force
    } else {
        $missed += $f
    }
}

if ($missed.Count -gt 0) {
    Write-Host "警告：找不到以下笔记文件（已跳过）："
    foreach ($m in $missed) { Write-Host "  $m" }
}

git add notes/
$diff = git status --porcelain
if ($diff) {
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "docs: 同步学习笔记 ($stamp)"
    git push
    if ($LASTEXITCODE -eq 0) {
        Write-Host "笔记已同步、提交并推送成功"
    } else {
        Write-Host "推送失败（可能是网络问题），可稍后手动执行：git push"
    }
} else {
    Write-Host "笔记内容无变化，跳过提交"
}