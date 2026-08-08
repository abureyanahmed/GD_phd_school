# Force-Directed Graph Layout

This project generates graph datasets and provides an interactive implementation of a force-directed graph layout algorithm.

## Project Workflow

The general workflow is:

1. Generate the dataset using `txt_to_json.py`.
2. Open `force_directed_method.html` in a web browser.
3. Initialize the graph and algorithm parameters using the browser console.
4. Execute the algorithm step-by-step to observe how the graph layout changes.

---

## 1. Generate the Dataset

To generate the dataset, run:

```bash
python .\txt_to_json.py
```

The script will prompt you to enter a file number:

```text
Enter file number:
```

Enter the number corresponding to the input file you want to process. For example:

```text
0
```

or:

```text
1
```

or:

```text
2
```

The generated dataset will then be used by the force-directed layout implementation.

---

## 2. Open the Force-Directed Method

After generating the dataset, open:

```text
force_directed_method.html
```

in a web browser.

The algorithm can be controlled interactively through the browser's developer console.

To open the developer console:

* **Chrome / Edge:** Press `F12` or `Ctrl + Shift + J`
* **Firefox:** Press `F12` or `Ctrl + Shift + K`

---

## 3. Define the Boundary

Before initializing the graph, define the boundary points.

For example:

```javascript
boundaryPoints.push(
    { x: 10, y: 15 },
    { x: 50, y: 15 },
    { x: 50, y: 60 },
    { x: 10, y: 60 }
);
```

These points define the boundary within which the graph layout is generated.

The boundary can be modified by changing the `x` and `y` coordinates.

---

## 4. Initialize the Algorithm

After defining the boundary, run the following commands in the browser console:

```javascript
init_k_temp()
init_nodes_links()
get_bfs_links()
```

These functions initialize the parameters and data structures required by the algorithm.

### `init_k_temp()`

Initializes the parameters related to the force-directed layout, including the initial temperature and other algorithm parameters.

### `init_nodes_links()`

Initializes the graph's nodes and links.

### `get_bfs_links()`

Processes the graph links using the BFS-related logic required by the implementation.

---

## 5. Run the Algorithm Step-by-Step

Once the graph has been initialized, the algorithm can be executed one step at a time.

### Get the Next Edge

Run:

```javascript
next_edge()
```

This advances the algorithm to the next edge being processed.

### Draw the Current Layout

Run:

```javascript
draw(non_isolated_nodes, links)
```

This draws the current graph layout using the current positions of the nodes and links.

### Perform One Iteration

Run:

```javascript
step(non_isolated_nodes, links)
```

This performs one iteration of the force-directed algorithm and updates the graph layout.

---

## 6. Typical Execution Sequence

A typical session in the browser console looks like this:

```javascript
boundaryPoints.push(
    { x: 10, y: 15 },
    { x: 50, y: 15 },
    { x: 50, y: 60 },
    { x: 10, y: 60 }
);

init_k_temp();
init_nodes_links();
get_bfs_links();

next_edge();
draw(non_isolated_nodes, links);
step(non_isolated_nodes, links);
```

After calling `step()`, the node positions are updated.

You can then call:

```javascript
draw(non_isolated_nodes, links);
```

again to visualize the updated layout.

Repeat the process as needed:

```javascript
next_edge();
step(non_isolated_nodes, links);
draw(non_isolated_nodes, links);
```

This allows the layout algorithm to be observed **iteration by iteration**.

---

## 7. Function Summary

| Function                          | Description                                                               |
| --------------------------------- | ------------------------------------------------------------------------- |
| `init_k_temp()`                   | Initializes the temperature and other force-directed algorithm parameters |
| `init_nodes_links()`              | Initializes the graph nodes and links                                     |
| `get_bfs_links()`                 | Obtains/processes the links used by the algorithm                         |
| `next_edge()`                     | Advances to the next edge                                                 |
| `draw(non_isolated_nodes, links)` | Draws the current graph layout                                            |
| `step(non_isolated_nodes, links)` | Executes one iteration of the force-directed algorithm                    |

---

## 8. Quick Start

For a quick run, follow these steps:

### Step 1 — Generate the dataset

```bash
python .\txt_to_json.py
```

Enter the desired file number when prompted:

```text
Enter file number:
```

### Step 2 — Open the HTML file

Open:

```text
force_directed_method.html
```

in a browser.

### Step 3 — Open the browser console

Open the developer console using `F12` or the appropriate keyboard shortcut.

### Step 4 — Initialize

Run:

```javascript
boundaryPoints.push(
    { x: 10, y: 15 },
    { x: 50, y: 15 },
    { x: 50, y: 60 },
    { x: 10, y: 60 }
);

init_k_temp();
init_nodes_links();
get_bfs_links();
```

### Step 5 — Execute the algorithm

Run:

```javascript
next_edge();
draw(non_isolated_nodes, links);
step(non_isolated_nodes, links);
```

Repeat `next_edge()`, `step()`, and `draw()` to continue processing and visualize each iteration.

---

## Notes

* Make sure the required dataset has been generated before running the HTML implementation.
* The `boundaryPoints` coordinates can be changed depending on the desired layout area.
* The algorithm is intended to be inspected interactively, so running `step()` one iteration at a time makes it possible to observe how the node positions evolve.
* The browser developer console is required for executing the interactive commands.
