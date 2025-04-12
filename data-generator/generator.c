#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N_STUDENTS (170)
#define N_CLASSES (4)

typedef struct class {
  int sections[N_CLASSES];
  int n_students[N_CLASSES];
} class_t;

int main() {
  class_t scla = { .sections = { 7, 9, 10, 12 }, { 50, 50, 50, 50 } };
  class_t econ = { .sections = { 10, 13, 14, 16 }, { 25, 100, 50, 50 } };
  class_t engr = { .sections = { 7, 8, 12, 14 }, { 50, 50, 100, 25 } };
  class_t cs = { .sections = { 9, 10, 11, 15 }, { 50, 25, 100, 50 } };
  class_t ma = { .sections = { 7, 8, 10, 13 }, { 50, 100, 50, 50 } };
  class_t chem = { .sections = { 9, 11, 12, 16 }, { 25, 50, 100, 50 } };
  class_t *classes[] = { &scla, &econ, &engr, &cs, &ma, &chem };

  srand(time(NULL));
  FILE *fp = fopen("test-cases.txt", "w");

  for (int i = 1; i <= N_STUDENTS; i++) {
    fprintf(fp, "#%d", i);

    for (int j = 0; j < N_CLASSES; j++) {
      bool valid = false;
      int section = -1;
      while (!valid) {
        section = rand() % N_CLASSES;
        if (classes[j]->n_students[section] - 1 >= 0) {
          valid = true;
          classes[j]->n_students[section]--;
        }
      }
      fprintf(fp, "-%d", classes[j]->sections[section]);
    }
    fprintf(fp, "\n");
  }

  fclose(fp);
  fp = NULL;
  return 0;
}

