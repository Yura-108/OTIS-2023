import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
import tkinter.colorchooser as colorchooser

# main
root = tk.Tk()
root.title("Graph")
main_label = tk.Label(root, text="Select an action")
main_label.pack(side=tk.BOTTOM)

# всякие переменные
click_num = 0
id_of_edge = 0
button1 = "<Button-1>"
num_vertex = "number of vertex"
id_text_global = "id text"
text_vertex = "text on vertex"

oval_id = None
ovals = []
edges = []
i = 0
id_text = 0
tag = 0
x1, y1, x2, y2 = 0, 0, 0, 0
cord_edge2 = {'id_vertex1': [], 'id_vertex2': []}
cord_edge = {'id_edge_text': [], 'id_vertex1': [], 'id_vertex2': []}
cord = {'id': [], id_text_global: [], text_vertex: [], 'textID': [], num_vertex: [], 'coordinatesX': [],
        'coordinatesY': []}
matrix_size = len(cord['id'])
matrix = [[0] * matrix_size for _ in range(matrix_size)]
tk.Tk.geometry(root, "800x600")
canvas = tk.Canvas(root, width=1920, height=1080)
canvas.pack()
menubar = tk.Menu(root)  # меню
root.config(menu=menubar)


# Function to handle drawing vertices
def draw_vertex_handler():
    main_label.configure(text="You have chosen to draw vertices, click on the free space to draw the vertex")
    canvas.unbind(button1)
    canvas.bind(button1, draw_canvas_handler)


# Function to handle drawing edges
def draw_edge_handler():
    main_label.configure(text="You have chosen to draw edges, click on the vertex to draw the edge")
    canvas.unbind(button1)
    canvas.bind(button1, draw_canvas_handler_second)


# Function to handle deleting vertices or edges
def delete_vertex_handler():
    main_label.configure(text="You have chosen to delete a vertex or edge, click on the vertex or edge to delete")
    canvas.unbind(button1)
    canvas.bind(button1, delete_canvas_handler)


# Function to handle renaming vertices
def rename_vertex_handler():
    main_label.configure(text="You have chosen to rename a vertex, click on the vertex to rename it")
    canvas.unbind(button1)
    canvas.bind(button1, rename_handler)


# Function to handle displaying information about vertices and edges
def edge_click_handler():
    print("Vertex")
    for key, value in cord.items():
        print(key, value)
    print("Edge")
    for value in cord_edge2.values():
        print(value, end=", ")


# Function to handle changing the color of vertices
def change_color_handler():
    main_label.configure(
        text="You have chosen to change the color of the vertex, click on the vertex to change its color")
    canvas.unbind(button1)
    canvas.bind(button1, colour_handler)


# Function to handle changing the text color of vertices
def change_text_color_handler():
    main_label.configure(
        text="You have chosen to change the color of the text, click on the vertex to change the color of its text")
    canvas.unbind(button1)
    canvas.bind(button1, text_colour_handler)


# Function to handle changing the color of edges
def change_edge_color_handler():
    main_label.configure(text="You have chosen to change the color of the edges, click on the edge to change its color")
    canvas.unbind(button1)
    canvas.bind(button1, edge_colour_handler)


# Function to handle deleting vertices or edges based on user click
def delete_canvas_handler(event):
    for x in ovals:
        if canvas.find_overlapping(event.x, event.y, event.x, event.y)[0] == x:
            # Delete the vertex
            canvas.delete(x)
            canvas.delete(cord['textID'][cord['id'].index(x)])
            ovals.remove(x)

            # Remove information about the vertex from data structures
            cord[num_vertex].remove(cord[num_vertex][cord['id'].index(x)])
            canvas.delete(cord[id_text_global][cord['id'].index(x)])
            cord['textID'].remove(cord['textID'][cord['id'].index(x)])
            cord[id_text_global].remove(cord[id_text_global][cord['id'].index(x)])
            cord["coordinatesX"].remove(cord['coordinatesX'][cord['id'].index(x)])
            cord["coordinatesY"].remove(cord['coordinatesY'][cord['id'].index(x)])
            cord[text_vertex].remove(cord[text_vertex][cord['id'].index(x)])
            cord['id'].remove(x)
            break  # Exit the loop after deleting the first matching vertex


# Function to handle drawing vertices
def draw_canvas_handler(event):
    global oval_id
    global i, tag, id_text
    id_text += 1
    i += 1
    itext = str(i)
    x, y = event.x, event.y
    tag = 'oval' + str(id_text)
    texttag = 'text' + str(id_text)

    # Store information about the vertex in the data structures
    cord[num_vertex].append(id_text)
    cord[id_text_global].append(tag)
    cord["coordinatesX"].append(x)
    cord["coordinatesY"].append(y)

    # Create oval (vertex) and text on canvas
    oval_id = canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill='green', tags=tag)
    ovals.append(oval_id)
    cord['id'].append(oval_id)
    canvas.create_text(x, y, text=itext, font="Arial 14", tags=texttag)
    cord['textID'].append(texttag)
    cord[text_vertex].append(itext)


# Function to handle drawing edges
def draw_canvas_handler_second(event):
    global click_num
    global x1, y1, x2, y2, id_of_edge
    if click_num == 0:
        # Select the first vertex for the edge
        for x in ovals:
            if canvas.find_overlapping(event.x, event.y, event.x, event.y)[0] == x:
                x1 = cord['coordinatesX'][cord['id'].index(x)]
                y1 = cord['coordinatesY'][cord['id'].index(x)]
                cord_edge['id_vertex1'].append(x)
                cord_edge2['id_vertex1'].append(x)
                click_num = 1
                main_label.configure(text="Select the second vertex to draw the edge")
    elif click_num == 1:
        # Select the second vertex and draw the edge
        for x in ovals:
            if canvas.find_overlapping(event.x, event.y, event.x, event.y)[0] == x:
                x2 = cord['coordinatesX'][cord['id'].index(x)]
                y2 = cord['coordinatesY'][cord['id'].index(x)]
                cord_edge['id_vertex2'].append(x)
                cord_edge2['id_vertex2'].append(x)
        tag_edge = 'edge' + str(id_of_edge)
        line = canvas.create_line(x1, y1, x2, y2, width=4, tags=tag_edge)
        edges.append(id_of_edge)
        cord_edge['id_edge_text'].append(tag_edge)
        id_of_edge += 1
        canvas.tag_lower(line)
        click_num = 0
        main_label.configure(text="Select a vertex to draw an edge on")


# Function to handle renaming vertices
def rename_handler(event):
    for x in ovals:
        if canvas.find_overlapping(event.x, event.y, event.x, event.y)[0] == x:
            # Prompt user for a new name
            new_name = simpledialog.askstring("Rename", "Enter new name")
            canvas.delete(cord['textID'][cord['id'].index(x)])

            # Create text with the new name on canvas
            canvas.create_text(cord['coordinatesX'][cord['id'].index(x)], cord['coordinatesY'][cord['id'].index(x)],
                               text=new_name, font="Arial 13", tags=(cord['textID'][cord['id'].index(x)]))

            # Update data structures with the new name
            cord[text_vertex][cord['id'].index(x)] = new_name
            break


def colour_handler(event):
    for x in ovals:
        if canvas.find_overlapping(event.x, event.y, event.x, event.y)[0] == x:
            new_colour = colorchooser.askcolor()
            color_hex = new_colour[1]
            canvas.itemconfig(x, fill=color_hex)
            break


def text_colour_handler(event):
    for x in ovals:
        if canvas.find_overlapping(event.x, event.y, event.x, event.y)[0] == x:
            new_colour = colorchooser.askcolor()
            color_hex = new_colour[1]
            canvas.itemconfig(cord['textID'][cord['id'].index(x)], fill=color_hex)
            break


def edge_colour_handler(event):
    for x in edges:
        tag_edge = 'edge' + str(x)
        if canvas.find_overlapping(event.x, event.y, event.x, event.y)[0] == canvas.find_withtag(tag_edge)[0]:
            new_colour = colorchooser.askcolor()
            color_hex = new_colour[1]
            canvas.itemconfig(tag_edge, fill=color_hex)
            break


def filling_matrix_handler():
    for i2 in range(len(cord_edge['id_vertex1'])):
        matrix[cord['id'].index(cord_edge['id_vertex1'][i2])][cord['id'].index(cord_edge['id_vertex2'][i2])] = 1
        matrix[cord['id'].index(cord_edge['id_vertex2'][i2])][cord['id'].index(cord_edge['id_vertex1'][i2])] = 1


def adjacency_matrix_handler():
    k = 0
    adj_matrix = tk.Tk()
    adj_matrix.title("Adjacency matrix")
    adj_matrix.geometry("250x250")

    filling_matrix_handler()
    for i3, val3 in enumerate(matrix):
        adj_matrix_label = tk.Label(adj_matrix, text=str(val3))
        adj_matrix_label.grid(row=k, column=0)
        i3 += 1
        print(i3)


def incidence_matrix_handler():
    k = 0
    inc_matrix = tk.Tk()
    inc_matrix.title("Incidence matrix")
    inc_matrix.geometry("250x250")

    for index in range(len(cord_edge['id_vertex1'])):
        matrix[cord['id'].index(cord_edge['id_vertex1'][index])][
            edges.index(cord_edge['id_edge_text'].index(cord_edge['id_edge_text'][index]))] = 1
        matrix[cord['id'].index(cord_edge['id_vertex2'][index])][
            edges.index(cord_edge['id_edge_text'].index(cord_edge['id_edge_text'][index]))] = 1
    for index2, value1 in enumerate(matrix):
        inc_matrix_label = tk.Label(inc_matrix, text=str(value1))
        inc_matrix_label.grid(row=k, column=0)
        k += 1
        index2 += 1
        print(index2)


def dfs_handler():
    visited = [False] * len(ovals)

    def dfs_rec_handler(vert):
        visited[vert] = True
        for u in range(len(ovals)):
            if matrix[vert][u] == 1 and not visited[u]:
                dfs_rec_handler(u)

    filling_matrix_handler()
    count = 0
    for v in range(len(ovals)):
        if not visited[v]:
            dfs_rec_handler(v)
            count += 1
    if count == 1:
        messagebox.showinfo("DFS", "Graph is connected")
    else:
        messagebox.showinfo("DFS", "Graph is not connected")


def bfs_handler():
    visited = [False] * len(ovals)

    def bfs_rec_handler(vert):
        visited[vert] = True
        for u in enumerate(ovals):
            if matrix[vert][u] == 1 and not visited[u]:
                bfs_rec_handler(u)

    filling_matrix_handler()
    count = 0
    for v in range(len(ovals)):
        if not visited[v]:
            bfs_rec_handler(v)
            count += 1
    if count == 1:
        messagebox.showinfo("BFS", "Graph is connected")
    else:
        messagebox.showinfo("BFS", "Graph is not connected")


# раздел меню
graphmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Graph", menu=graphmenu)
# кнопки в разделе меню
graphmenu.add_command(label="Draw a vertex", command=draw_vertex_handler)
graphmenu.add_command(label="Draw an edge", command=draw_edge_handler)
graphmenu.add_command(label="Removing vertices or edges", command=delete_vertex_handler)

redmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Editing", menu=redmenu)
redmenu.add_command(label="Rename a vertex", command=rename_vertex_handler)
redmenu.add_command(label="Repaint the vertex", command=change_color_handler)
redmenu.add_command(label="Recolor text", command=change_text_color_handler)
redmenu.add_command(label="Repaint an edge", command=change_edge_color_handler)

algmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Algorithms", menu=algmenu)
algmenu.add_command(label="Output the adjacency matrix", command=adjacency_matrix_handler)
algmenu.add_command(label="Output the incidence matrix", command=incidence_matrix_handler)
algmenu.add_command(label="Search in depth", command=dfs_handler)
algmenu.add_command(label="Search in width", command=bfs_handler)

root.mainloop()
