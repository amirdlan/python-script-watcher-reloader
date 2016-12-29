Hot-reload of Python scripts
============================

Watch a folder of scripts, import or reload each of them upon external change
(i.e. you edit the file).  Once imported, run a predefined function on that
[re]imported module.

## What is it good for? (Use Cases)

 You have a script that **procedurally generates an image**. You can have
 your watcher reload the script and execute the generation function without
 re-running the whole app. This __greatly improves productivity__ as you
 don't have to manually generate the image each time from the command line.

 When developing a game, you have **your entities' behavior defined in Python
 scripts** (because you don't like Lua). A watcher and module hot-reloading
 can __greatly enhance the prototyping phase__ of the game (this only happens
 in development, you don't want that to happen when the game is shipped.
 o'rly? Maybe you want amazing modding abilities! But that's a discussion for
 a different scope).