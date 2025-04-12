#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N_STUDENTS (264)
#define N_CLASSES (8)
#define N_SECTIONS (4)
#define N_PREFERENCES (3)
#define N_POINTS (10)

typedef enum day {
  TR, MWF
} day_t;

typedef struct class {
  int sections[N_CLASSES];
  int n_students[N_CLASSES];
} class_t;

bool is_free_time(int *arr, day_t *days, int time, int index) {
  bool exit_code = true;
  for (int i = 0; i < N_CLASSES; i++) {
    if (days[index] == days[i] && arr[i] == time) {
      exit_code = false;
      break;
    }
  }
  return exit_code;
}

void print_pref_arr(FILE *fp) {
  int arr[N_PREFERENCES] = { 0 };
  int sum = 0;
  for (int i = 0; i < N_PREFERENCES; i++) {
    int rand_n = rand() % (N_PREFERENCES + 1);
    arr[i] = rand_n;
    sum += rand_n;
  }

  if (sum < N_POINTS) {
    arr[rand() % N_PREFERENCES] += N_POINTS - sum;
  } 

  for (int i = 0; i < N_PREFERENCES; i++) {
    fprintf(fp, "|%d", arr[i]);
  }
}

int main() {
  class_t scla = { .sections = { 7, 9, 10, 12 }, { 50, 50, 50, 50 } };
  class_t econ = { .sections = { 10, 13, 14, 16 }, { 25, 100, 50, 50 } };
  class_t engr = { .sections = { 7, 8, 12, 14 }, { 50, 50, 100, 25 } };
  class_t cs = { .sections = { 9, 10, 11, 15 }, { 50, 25, 100, 50 } };
  class_t ma = { .sections = { 7, 8, 10, 13 }, { 50, 100, 50, 50 } };
  class_t chem = { .sections = { 9, 11, 12, 16 }, { 25, 50, 100, 50 } };
  class_t pol = { .sections = { 8, 9, 10, 13 }, { 25, 100, 50, 50 } };
  class_t hist = { .sections = { 10, 13, 14, 16 }, { 25, 50, 100, 50 } };
  class_t *classes[] = { &scla, &econ, &engr, &cs, &ma, &chem, &pol, &hist };
  day_t days[] = { TR, TR, TR, MWF, MWF, MWF, TR, MWF };

  srand(time(NULL));
  FILE *fp = fopen("test-cases.txt", "w");

  for (int i = 1; i <= N_STUDENTS; i++) {
    fprintf(fp, "#%d", i);

    for (int j = 0; j < N_CLASSES; j++) {
      if (rand() % 4 == 0) {
        fprintf(fp, "-%d", 0);
        continue;
      }
      int arr[N_CLASSES] = { 0 };

      bool valid = false;
      int section = -1;
      while (!valid) {
        section = rand() % N_SECTIONS;
        if (classes[j]->n_students[section] - 1 >= 0 && is_free_time(arr, days, classes[j]->sections[section], j)) {
          valid = true;
          classes[j]->n_students[section]--;
        }
      }
      fprintf(fp, "-%d", classes[j]->sections[section]);
    }

    print_pref_arr(fp);
    fprintf(fp, "\n");
  }

  fclose(fp);
  fp = NULL;
  return 0;
}

