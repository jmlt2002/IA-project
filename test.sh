#!/bin/bash

# Define the paths to the Python script, input file, and expected output file
python_script="bimaru.py"
expected_output_prefix="instances-students/instance"

# Iterate over the file names from 1 to 10
for ((i = 1; i <= 10; i++)); do
    file_number=$(printf "%02d" $i)
    input_file="instances-students/instance${file_number}.txt"
    expected_output_file="${expected_output_prefix}${file_number}.out"
    output_file="output_${file_number}.txt"
    start_time=$(date +%s.%N)
    # Run the Python script with the input file and save the output to a temporary file
    python3 "$python_script" < "$input_file" > "$output_file"
    end_time=$(date +%s.%N)
    execution_time=$(echo "$end_time - $start_time" | bc)


    # Compare the output file with the expected output file using the `diff` command
    diff -u "$expected_output_file" "$output_file" > /dev/null

    # Check the exit code of diff to determine if the output matches the expected output
    if [ $? -eq 0 ]; then
        echo -e "\e[32mOutput for Test $i matches the expected output!\e[0m with execution time: $execution_time"
    else
        echo -e "\e[31mOutput for Test $i does not match the expected output:\e[0m with execution time: $execution_time"
        diff --color=always -u "$expected_output_file" "$output_file"
    fi

    # Clean up by removing the temporary output file
    rm "$output_file"
done