scoreboard objectives add Var dummy
scoreboard players set .Value Var 0
execute as @a at @s run function namespace:increase_value {"amount": 1}
execute as @a at @s run function namespace:increase_value {"amount": 2}
execute as @a at @s run function namespace:increase_value {"amount": 3}
execute as @a at @s run function namespace:increase_value {"amount": 4}
execute as @a at @s run function namespace:increase_value {"amount": 5}
execute as @a at @s run function namespace:increase_value {"amount": 6}
execute as @a at @s run function namespace:increase_value {"amount": 7}
execute as @a at @s run function namespace:increase_value {"amount": 8}
execute as @a at @s run function namespace:increase_value {"amount": 9}
execute as @a at @s run function namespace:increase_value {"amount": 10}
function namespace:macroscores/var