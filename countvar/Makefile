GCC=gcc


ALL_TARGETS = countvar 

all: $(ALL_TARGETS)

countvar: countvar.c util.c
	$(GCC) $^ -o $@

clean:
	rm -f $(ALL_TARGETS)
	rm -f *~

