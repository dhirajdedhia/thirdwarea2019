Function StateCityExtract()
	dim vString
	
	vString  = WScript.Arguments.Item(0)
	'vString  = "NORTH HAVEN, CT 06473-1138"
	
	vString  = Trim(vString)
	
	'Removing Extra Spaces
	Do While InStr(1, vString, "  ")
	vString = Replace(vString, "  ", " ")
	Loop
	msgbox vString
	
	'Reversing the String
	vReverse = strReverse(vString)
	vCount = 1
	
	for i = 1 to len(vReverse)
		vLetter  = Mid(vReverse,i,1)
		vBoolean = IsNumeric(vLetter)
		if (vBoolean = TRUE) or vLetter = "-" Then
			vCount = vCount + 1
		End if
		If vLetter = " " Then
			exit For
		End if
	Next
	
	vZipCode = Mid(vReverse,1,vCount)
	vZipCode = strReverse(vZipCode)
	vZipCode = Trim(vZipCode)
	
	vRemain  = Mid(vReverse,vCount)
	vRemain  = Trim(vRemain)
	
	vState   = Mid(vRemain,1,2)
	vState   = strReverse(vState)
	vState   = replace(vState,",","")
	vState   = Trim(vState)
	
	vCity    = Mid(vRemain,3)
	vCity    = strReverse(vCity)
	vCity    = replace(vCity,",","")
	vCity    = Trim(vCity)
	
	StateCityExtract =  vCity + "|" + vState + "|" + vZipCode
	
	WScript.StdOut.WriteLine (StateCityExtract)
	
	msgbox (vZipCode)
	msgbox (vState)
	msgbox (vCity)
End Function