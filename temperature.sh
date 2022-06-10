#!/bin/bash
 
# Guardamos el valor de temperatura de la CPU a una variable
cpuTemp=$(cat /sys/class/thermal/thermal_zone0/temp)

curl http://app.biosabor.com:8088/v1/fincas/temperatura/$((cpuTemp/1000))