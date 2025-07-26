arg := A_Args[1]
if !arg {
    MsgBox("No argument passed.")
    ExitApp()
}

specialModifiers := "^!+#"
heldKeys := []

HoldKey(key) {
    global heldKeys
    if !heldKeys.Has(key) { ; Only hold down the key if it isnt already being held
        Send("{" key " down}")
        heldKeys.Push(key)
    }
}

ReleaseHeldKeys() { ; Releases all keys from cache
    global heldKeys
    for key in heldKeys {
        Send("{" key " up}")
    }
    heldKeys := []
}

SendCombo(keys) { ; Holds down all keys in cache, and releases after it finishes
    for key in keys
        HoldKey(key)
    Sleep(50)
    ReleaseHeldKeys()
}

isKeybind := false
isText := false

comboKeys := []
characters := 0

pos := 1
len := StrLen(arg)

while pos <= len { ; While the arg hasn't been gone through
    char := SubStr(arg, pos, 1)

    if InStr(specialModifiers, char) {
        isKeybind := true ; Uses keybinds

        ; Convert special characters to keys, so they can be held down
        if char = "^"
            comboKeys.Push("Control")
        else if char = "!"
            comboKeys.Push("Alt")
        else if char = "+"
            comboKeys.Push("Shift")
        else if char = "#"
            comboKeys.Push("LWin")
        pos++

    } else if char = "{" {
        endPos := InStr(arg, "}", , pos)
        if !endPos
            ExitApp()

        keyName := SubStr(arg, pos + 1, endPos - pos - 1) ; Gets the name of the key, without braces
        comboKeys.Push(keyName) ; The keys are already defined, so we add it here
        isKeybind := true ; Uses keybinds
        pos := endPos + 1

    } else { ; None of them match, so its regular content
        characters++
        if characters > 1 ; Only allow 1 character so keybinds like win+r (#r) work
            isText := true ; If its more than one, turn isText true (Keybinds and regular characters dont mix)

        else {
            comboKeys.Push(char)
        }
        pos++
    }
}

if isKeybind && isText { ; If they're both on, they use both types (which isnt allowed)
    ExitApp() ; prevent mixing input types
}

if isKeybind {
    SendCombo(comboKeys)

} else {
    ; pure text input
    pos := 1
    while pos <= len { ; Add a small delay for adding text to make sure no unexpected error occurs
        char := SubStr(arg, pos, 1)
        Send(char)
        Sleep(50)
        pos++
    }
}

Sleep(100)
ExitApp()
