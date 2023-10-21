#!/bin/bash

list_variable=("cloud_cover" "snow_thickness_lwe" "2m_temperature" "2m_dewpoint_temperature" "snow_thickness" "vapour_pressure" "10m_wind_speed")
list_mounth=("01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12")
list_year=("2018" "2019" "2020" "2021" "2022" "2023")
script_python="CDSAPI_VAR_METEREOLOGICAS.py"

for variable in "${list_variable[@]}"; do
    for year in "${list_year[@]}"; do
        for mounth in "${list_mounth[@]}"; do
            sudo /usr/bin/python3 "$script_python" "$mounth" "$year" "$variable" | tee salida_ejecucion.txt
            sleep 10
done    
done
done