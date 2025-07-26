key := A_Args[1]
duration := A_Args[2]

if !key or !duration {
    MsgBox("Invalid arguments passed.")
    ExitApp()
}

Send("{" key " down}")
Sleep(duration * 1000)
Send("{" key " up}")

ExitApp()
