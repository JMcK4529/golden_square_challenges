# Process Log


## What should Diary do?

### Diary.__init__()
- Should create an instance variable "Diary.entry_list" which will be used to store all the entries.

### Diary.add()
- We should be able to add DiaryEntry instances to the Diary.
- The method should return nothing, but should store each DiaryEntry added to an instance variable (should it be private?).

### Diary.all()
- Should return a list of DiaryEntry instances.
- This should probably be a list of titles, so it is in a user-readable format.
- Will make use of DiaryEntry's variable "DiaryEntry.title".

### Diary.count_words()
- Should return an integer equal to the total number of words contained in all the DiaryEntry instances (titles and contents included).
- Will make use of DiaryEntry's method "DiaryEntry.count_words()".

### Diary.reading_time(wpm)
- Should return an integer: the time in minutes it would take to read every DiaryEntry in the Diary with a reading speed of "wpm" words per minutes.
- Will make use of DiaryEntry's method "DiaryEntry.reading_time()".

### Diary.find_best_entry_for_reading_time(wpm, minutes)
- Should return the DiaryEntry instance which contains 
- The DiaryEntry should be the one which has the reading time closest to (but not beyond) "minutes".
- Will make use of DiaryEntry's method "DiaryEntry.reading_time()".


## What should DiaryEntry do?

### DiaryEntry.__init__(title, contents)
- Should create instance variables "DiaryEntry.title" and "DiaryEntry.contents".
- Should also create an instance variable to keep track of chunks "DiaryEntry.chunked_so_far".

### DiaryEntry.count_words()
- Should return an integer: the number of words in the DiaryEntry.

### DiaryEntry.reading_time(wpm)
- Should return an integer: the number of minutes it would take to read "DiaryEntry.contents" at a reading speed of "wpm" words per minute.
- Will make use of "DiaryEntry.count_words()".

### DiaryEntry.reading_chunk(wpm, minutes)
- Should return a chunk of "DiaryEntry.contents" which could be read in "minutes" minutes at a reading speed of "wpm" words per minute.