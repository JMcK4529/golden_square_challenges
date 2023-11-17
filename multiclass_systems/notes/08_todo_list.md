# Process Log


## What should ToDoList do?

### ToDoList.__init__()
- Create an instance variable "ToDoList.todo_list" to track ToDo instances added to ToDoList.

### ToDoList.add(todo)
- Store an instance of ToDo "todo" to the self.object in self.todo_list.
- Return nothing.

### ToDoList.incomplete()
- Returns a list of ToDo instances which have not yet undergone the "ToDo.mark_complete()" method.
- Will make use of a Boolean instance variable in the ToDo object called "ToDo.complete".

### ToDoList.complete()
- Returns a list of ToDo instances which have undergone the "ToDo.mark_complete()" method.
- Will make use of a Boolean instance variable in the ToDo object called "ToDo.complete".

### ToDoList.give_up()
- Returns nothing, but calls "ToDo.mark_complete()" on every instance of ToDo currently stored in the ToDoList which is not yet complete.
- Will make use of the "ToDo.complete" attribute and the "ToDo.mark_complete()" method.

## What should ToDo do?

### ToDo.__init__(task)
- Create an instance variable (string) called "ToDo.task" which stores the task name.
- Create an instance variable (Boolean) called "ToDo.complete" which stores the completion state of the ToDo instance.

### ToDo.mark_complete()
- Returns nothing, but sets the "ToDo.complete" attribute to True.