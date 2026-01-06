# Written by Siep Kroonenberg in 2024 and placed in the Public Domain.
# This is a Powershell version of psviewer.vbs, created because vbscript
# Since vbscript is no longer a guaranteed component of windows,
# I created this powershell version.

Add-Type -AssemblyName PresentationFramework

# note. win10 has PS version >= 5

if ($args.count -lt 1) {
  $msg = @"
Psviewer is a simple script which converts its argument to a
temporary pdf and displays it in the default pdf viewer.

Double-clicking an .eps- or .ps file should result in viewing the
converted file. If this does not work, then try right-click and
'Open with', which should give you the option to pick psviewer and
set it as default program for .[e]ps files.
"@
  [System.Windows.MessageBox]::Show($msg, 'Missing argument', 'OK', 'Hand')
  exit 1
}
$f = $args[0]
if (-not (test-path -path $f -pathtype leaf)) {
  [System.Windows.MessageBox]::Show(
    "$f does not exist", 'Error', 'OK', 'Hand')
  exit 1
}
$f = $f.replace("\", "/")
$p = split-path -path $f -leaf -resolve

# find suitable name for to be generated pdf.
# do it manually; no options for filename templates
# with the new-temporaryfile cmdlet
$i=0
$success = $false
do {
  $i++
  $r = get-random -min 0 -max 1000000
  $pdf = $("{0:000000}" -f $r)
  # we want to see the original filename in the viewer's titlebar
  $pdf = $p + '___' + $pdf + '.pdf'
  # new-item will fail if $pdf already exists
  $success = (new-item -path "$env:temp" -name $pdf -ea "ignore")
} until ($success -or ($i -ge 500))
if (-not $success) {
  [System.Windows.MessageBox]::Show(
    "Could not create temporary pdf", 'Error', 'OK', 'Hand')
  exit 1
}
$pdf = "${env:temp}\$pdf"
$pdf = $pdf.replace("\", "/")

# create the temporary pdf, which is as yet just an empty file
# exit codes are not always reliable; test instead for non-empty output
if ($p -ilike "*.eps") {
  if (kpsewhich -format texmfscripts epstopdf.pl) {
    epstopdf "$f" "$pdf"
  }
  if ((get-item $pdf).length -eq 0) {
      rungs -q -dNOPAUSE -dBATCH -P- -dSAFER -sDEVICE#pdfwrite -dEPSCrop -sOutputFile#"$pdf" -f "$f"
  }
}
if ((get-item $pdf).length -eq 0) {
  # eps treatment has failed or has not been attempted
  rungs -q -dNOPAUSE -dBATCH -P- -dSAFER -sDEVICE#pdfwrite -sOutputFile#"$pdf" -f "$f"
}

if ((get-item $pdf).length -eq 0) {
  [System.Windows.MessageBox]::Show(
    "Could not convert to temporary pdf; invalid PostScript?", 'Error', 'OK', 'Hand')
  exit 1
}
invoke-item -path $pdf
exit 0
