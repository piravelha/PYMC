Hi! Thanks for downloading and using my PythonMC datapack template!

# Main Topics

In this file, you will learn how to use PythonMC to improve your datapack creation experience.

This guide will cover the basic syntax of .mcpy files, how to run it using python, and key features of PythonMC.

# Getting Started

First, you have to download python. There are many guides out there, so find one you are comfortable with and follow it.

After installing python and making sure to enable the system variable path for it, check that you have the main folder of your datapack open in your IDE, and run the following command to compile your test datapack:

```bs
python data/python/compiler.py
```

After that, you can test it on minecraft, it should display a simple "Reloaded!" text in the chat.

# Editing your datapack

The .mcpy files of your datapack are stored in the `data/python/functions` folder, where you can create new functions, or edit the ones that already exist.

Every .mcpy file has to start out with a PATH comment, that specifies where in the datapack the function is compiled to. The PATH comment's path should not specify the namespace, it will generate them in the namespace specified in the compiler file.

* Example (Will compile it to `NAMESPACE:load`):

![image](https://github.com/piravelha/PYMC/assets/140568241/e31086cb-4219-476d-a730-69262bfb7c3a)

# Basic Syntax

The syntax of PythonMC is pretty straightfoward, being very similar to Minecraft's.

## Slash Commands

To run a basic slash command, all you have to do is write a slash `/`, followed by your command

* Example:

![image](https://github.com/piravelha/PYMC/assets/140568241/e12ecf86-8b10-4c7a-bd43-7cd1f369585d)


## Linebreaks, EVERYWHERE!

You can add linebreaks pretty much everywhere, without much restriction, here are a few examples:

![image](https://github.com/piravelha/PYMC/assets/140568241/cc5abc41-2e2b-4710-a30d-c2bef1270e85)

---

![image](https://github.com/piravelha/PYMC/assets/140568241/d34405cd-c180-451c-8947-17975ceb9bf0)

## Creating Functions

To create a new function, you can write `/mcfunction` followed by the name of your function, followed by an open bracket and a line break.

Inside the function you can write more slash commands as usual, and to call the function, you can just use the regular `/function` command from minecraft.

The function will be stored on the directory `NAMESPACE:function_name`, so if your function name is `test/my_function` it will be put inside a folder called `test`

* Example:

![image](https://github.com/piravelha/PYMC/assets/140568241/d6f4089a-07be-4f90-8305-ea0d4969806e)


## Macros

Macros are a very useful feature available in the latest version of Minecraft, this guide will not be covering them, but they are available inside PythonMC.

* Using a Macro Command inside a regular function file:

![image](https://github.com/piravelha/PYMC/assets/140568241/54ec4058-a7c7-4aa7-95ad-d6c6bd400684)

* Using a Macro Command inside an mcfunction:

![image](https://github.com/piravelha/PYMC/assets/140568241/e4b94898-f327-4991-b6fc-24a6abb12e1d)

## Percent (%) Functions (BETA)

Percent Functions are currently a BETA feature, and allow you to a few things that will could do otherwise, but in a cleaner way.

There are currently two working Percent Functions:

* `/%macroscore`
* `/%timer`

### MacroScore

The MacroScore % Function allows you to call a function passing one or more scoreboard values as macros directly, instead of needing to store them inside a data storage and using it.

When acessing the scoreboard values as macros, the name of the macro will be integers starting at `1`, and increasing for every other additional score parsed as an argument

### Syntax:
![image](https://github.com/piravelha/PYMC/assets/140568241/2c54bb22-d949-40ad-abd2-c9ec7bf0e873)

* Example:

![image](https://github.com/piravelha/PYMC/assets/140568241/bdcf0571-4c4f-48b6-b2f4-feb37bdc0456)


## Timer

The Timer % Function gives you more practicality than the `/schedule` command, since it allows you to maintain the entity that is running the command, in which the `/schedule` command just runs it on the server

### Syntax

The syntax of the loop command is straight forward, by writing out `/%timer` followed by the function to call, and a delay which can be specified in:

* `0t`: `ticks`
* `0s`: `seconds`
* `0m`: `minutes`
* `0d`: `minecraft days`
* `0h`: `hours`


![image](https://github.com/piravelha/PYMC/assets/140568241/4a07096c-a578-404b-bb17-f9c16264673d)


> NOTE: The timer percent command currently does not support Macros

### Examples

![image](https://github.com/piravelha/PYMC/assets/140568241/70bfd521-8ebd-40ff-98ba-f25191841ad1)
