---
coverY: 0
---

# Interacting with OpenLoop io

OpenLoop's `io` runtime variable has some deprecated or mostly unused functions but is essentail to use for configurating settings and databases (Not reccomended for bigger applications but great for configs).

### Workers

```python
def hi():
    print("Hello World")

io.worker(hi, 6000) # Prints Hello World every 6000ms
```

Workers run under the baked-in `threading` module inside of Python, so it's only good for IO tasks and not heavy tasks.

### Publishing

```python
io.publish("My Friends", "Joe")
-> Would make your real database be {"My Friends": ["Joe"]}
```

This is normally not needed unless you want to use the built-in Database, try to keep the data low if you are because your device may get performance hindered while saving.

#### Generating Origin

```python
def do_something():
    io.publish("My Friends", "Joe")
    io.generate_origin() # This will publish in origin the current date
    
io.worker(do_something, 6000)
```

