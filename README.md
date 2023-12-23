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
```
# PATH: load
```

# Basic Syntax

The syntax of PythonMC is pretty straightfoward, being very similar to Minecraft's.

## Slash Commands

To run a basic slash command, all you have to do is write a slash `/`, followed by your command

* Example:
```mcpy
# PATH: load

/say Hello World!
```

## Linebreaks, EVERYWHERE!

You can add linebreaks pretty much everywhere, without much restriction, here are a few examples:

```
# PATH: load

/execute as 
    @a[
        tag = shouldGetSword
    ] 
    run give 
    @s netherite_sword{
        display: {
            Name: '{
                "text": "My Custom Sword",
                "color": "dark_purple",
                "bold": true,
                "italic":false
            }',
            Lore: ['{
                "text": "This is my very powerful custom sword",
                "color": "gray",
                "italic": false
            }']
        },
        Enchantments:[
            {id:"minecraft:sharpness",lvl:6s},
            {id:"minecraft:fire_aspect",lvl:5s},
            {id:"minecraft:looting",lvl:2s},
            {id:"minecraft:unbreaking",lvl:4s}
        ]
    } 1
```

```
# PATH: load

/tellraw @a [
    {
        "text": "Hello! ",
        "color":"green"
    },
    {
        "text": "How are you doing?",
        "color":"aqua",
        "hoverEvent": {
            "action": "show_text",
            "value": [{
                "text":"This is a custom hover text!",
                "italic": true,
                "underlined": true
            }]
        }
    }
]
```

## Creating Functions

To create a new function, you can write `/mcfunction` followed by the name of your function, followed by an open bracket and a line break.

Inside the function you can write more slash commands as usual, and to call the function, you can just use the regular `/function` command from minecraft.

The function will be stored on the directory `NAMESPACE:function_name`, so if your function name is `test/my_function` it will be put inside a folder called `test`

* Example:
```mcpy
# PATH: load

/mcfunction my_function {
    /say This code is being ran inside a function!
}

/function NAMESPACE:my_function
```

## Macros

Macros are a very useful feature available in the latest version of Minecraft, this guide will not be covering them, but they are available inside PythonMC.

* Using a Macro Command inside a regular function file:
```
# PATH: macro_function

/$say The value is $(value)
```

* Using a Macro Command inside an mcfunction:
```
# PATH: load

/mcfunction macro_test {
    /$say The value is $(value)
}

/function NAMESPACE:macro_test 
    {"value": 15}
```

## Percent (%) Functions (BETA)

Percent Functions are currently a BETA feature, and allow you to a few things that will could do otherwise, but in a cleaner way.

There are currently two working Percent Functions:

* `/%macroscore`
* `/%timer`

### MacroScore

The MacroScore % Function allows you to call a function passing one or more scoreboard values as macros directly, instead of needing to store them inside a data storage and using it.

When acessing the scoreboard values as macros, the name of the macro will be integers starting at `1`, and increasing for every other additional score parsed as an argument

### Syntax:
```
/%macroscore NAMESPACE:<filepath> <selector> <scoreboard> | .. | <selector> <scoreboard>
```

* Example:

```
# PATH: load

/scoreboard objectives add Vars dummy
/scoreboard players set .TestVar Vars 73

/mcfunction print_test_var {
    /$say TestVar is currently set to $(vars)
}

/%macroscore NAMESPACE:print_test_var .TestVar Vars
```

## Timer

The Timer % Function gives you more practicality than the `/schedule` command, since it allows you to maintain the entity that is running the command, in which the `/schedule` command just runs it on the server

### Syntax

The syntax of the loop command is straight forward, by writing out `/%timer` followed by the function to call, and a delay which can be specified in:

* `0t`: `ticks`
* `0s`: `seconds`
* `0m`: `minutes`
* `0d`: `minecraft days`
* `0h`: `hours`

```
/%timer <function> <delay>
```

> NOTE: The timer percent command currently does not support Macros

### Examples
```
# PATH: load

/%timer namespace:timer_test 10s
```
