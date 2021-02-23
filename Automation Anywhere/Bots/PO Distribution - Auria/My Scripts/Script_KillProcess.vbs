strComputer = "."

Process = WScript.Arguments.Item(0)

Set objWMIService = GetObject("winmgmts:" & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2") 
Set colProcess = objWMIService.ExecQuery ("Select * from Win32_Process Where Name like '" & Process & "%'")
For Each p in colProcess
  On Error Resume Next
          p.Terminate   
  On Error GoTo 0          
Next
SET objWMIService = Nothing
SET colProcess = Nothing