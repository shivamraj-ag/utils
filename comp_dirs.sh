#!/bin/bash

# Check if two arguments (directories) are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <directory1> <directory2>"
    exit 1
fi

DIR1="$1"
DIR2="$2"

# Check if both arguments are valid directories
if [ ! -d "$DIR1" ] || [ ! -d "$DIR2" ]; then
    echo "Error: Both inputs must be directories."
    exit 1
fi

echo "Comparing directories: $DIR1 and $DIR2"
echo "----------------------------"

# Find files with specific extensions and sort for comparison
find "$DIR1" -type f \( -name "*.h" -o -name "*.cpp" -o -name "*.inl" -o -name "*.lua" \) | sed "s~$DIR1~~g" | sort > /tmp/files1.txt
find "$DIR2" -type f \( -name "*.h" -o -name "*.cpp" -o -name "*.inl" -o -name "*.lua" \) | sed "s~$DIR2~~g" | sort > /tmp/files2.txt

# Find missing files
echo "Files only in $DIR1:"
while read file; do
    if [ ! -f "$DIR2/$file" ]; then
        echo "$file"
    fi
done < /tmp/files1.txt 

echo "----------------------------"
echo "Files only in $DIR2:"
while read file; do
    if [ ! -f "$DIR1/$file" ]; then
        echo "$file"
    fi
done < /tmp/files2.txt

echo "Files that exist in both but are different:"

echo "----------------------------"


while read -r f ; do 
    if ! cat /tmp/files2.txt | grep -q "$f"; then
        continue
    fi
    if ! cmp -s "$DIR1/$f" "$DIR2/$f"; then
        echo "$DIR1/$f $DIR2/$f"
    fi
done < /tmp/files1.txt
echo "----------------------------"

# Clean up
rm -f /tmp/files1.txt /tmp/files2.txt
