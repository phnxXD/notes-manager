import PySimpleGUI as sg

# Define the layout of the GUI
layout = [
    [sg.Text('Name:'), sg.InputText(key='name')],
    [sg.Text('Note:'), sg.Multiline(key='note', size=(60, 5), font=('Helvetica', 12))],
    [sg.Button('Save'), sg.Button('Search'), sg.Button('Exit')],
    [sg.Text('Search:'), sg.InputText(key='search')],
    [sg.Listbox(values=[], size=(60, 10), key='notes')],
    [sg.Button('Edit'), sg.Button('Delete')],
]

# Create the window
window = sg.Window('Note Taker', layout)

# Open the file to save notes
with open('notes.txt', 'a+') as f:
    # Read the existing notes from the file
    f.seek(0)
    notes = f.readlines()
    notes = [note.strip() for note in notes]

    # Loop to process events
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        if event == 'Save' or (event == 'note' and '\n' in values['note']):
            name = values['name']
            note = values['note']
            # Write the note to the file
            try:
                f.write(f'{name}: {note}\n')
                # Append the new note to the list
                notes.append(f'{name}: {note}')
                # Clear the input fields
                window['name'].update('')
                window['note'].update('')
            except Exception as e:
                # Show an error dialog box with the error message and option to copy
                sg.popup_error(f'Error: {e}\n\nCopy the error message with Ctrl+C', keep_on_top=True)
        if event == 'Search':
            search_term = values['search']
            # Search for notes that contain the search term
            matching_notes = [note for note in notes if search_term.lower() in note.lower()]
            # Update the listbox with the matching notes
            window['notes'].update(values=matching_notes)
        if event == 'Edit':
            # Get the selected note from the listbox
            selected_note = window['notes'].get()[0]
            # Extract the name and note text from the selected note
            selected_name, selected_text = selected_note.split(': ', 1)
            # Update the input fields with the selected note
            window['name'].update(selected_name)
            window['note'].update(selected_text)
            # Remove the selected note from the list of notes
            notes.remove(selected_note)
            # Update the listbox with the remaining notes
            window['notes'].update(values=notes)
        if event == 'Delete':
            # Get the selected note from the listbox
            selected_note = window['notes'].get()[0]
            # Remove the selected note from the list of notes
            notes.remove(selected_note)
            # Update the listbox with the remaining notes
            window['notes'].update(values=notes)
            # Remove the selected note from the file
            f.seek(0)
            f.truncate()
            f.writelines([note + '\n' for note in notes])

    # Update the listbox with all notes after the window is fully created
    window['notes'].update(values=notes)

    # Close the file
    f.close()

# Close the window
window.close()
