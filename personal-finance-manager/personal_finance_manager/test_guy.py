import FreeSimpleGUI as sg

# We define the "layout": a list of lists.
# Each inner list is a ROW in the window.
layout = [
    [sg.Text("Hello, Maurizio!")],
    [sg.Button("OK")]
]

# We create the window with a title and the layout we defined
window = sg.Window("My First Window", layout)

# This is the "event loop": the window stays listening
# for what the user does (button click, closing the window, etc.)
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "OK":
        break

window.close()