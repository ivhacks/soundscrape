#!/bin/bash
python -m unittest test_bandcamp_search.py test_beatport_search.py test_sevendigital_search.py -v

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
else
    echo ""
    echo "❌ Some tests failed!"
    exit 1
fi 