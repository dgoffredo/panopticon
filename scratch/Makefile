# Specify BEGIN and END using make syntax, e.g.
#
#     make BEGIN=2012-01-01 END=2012-04-01
#
# Their format is an ISO 8601 date.
# If unspecified, they have suitably past and future values, respectively.
BEGIN ?= 0001-01-01
END ?= 9999-01-01

# If a recipe fails, delete its target.
.DELETE_ON_ERROR:

.PHONY: show clean totals.svg

show: totals.svg
	firefox totals.svg &

totals.svg: totals.plt totals.sql ../database.sqlite3
	sed "s/?1/'$(BEGIN)'/g" totals.sql | \
		sed "s/?2/'$(END)'/g" | \
		sqlite3 ../database.sqlite3  | \
		awk -F '|' '{print NR-1, $$1, $$2}' | \
		gnuplot totals.plt > totals.svg

clean:
	rm -f totals.svg 2>/dev/null
