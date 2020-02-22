#!/bin/bash

run() {
    pypy3 code.py  "$1" < "$1" > "$2" &
    pids[$3]=$!
    #echo "finished $1"
}

run "a_example.txt" "a_out_1" 0
run "b_read_on.txt" "b_out_1" 1
run "c_incunabula.txt" "c_out_1" 2
run "d_tough_choices.txt" "d_out_1" 3
run "e_so_many_books.txt" "e_out_1" 4
run "f_libraries_of_the_world.txt" "f_out_1" 5

for pid in ${pids[*]}; do
    wait $pid
done

echo "all done"

exit 0