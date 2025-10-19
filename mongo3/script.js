document.addEventListener('DOMContentLoaded', () => {
    const todoForm = document.getElementById('todo-form');
    const todoList = document.getElementById('todo-list');
    const nameInput = document.getElementById('name');
    const descriptionInput = document.getElementById('description');

    const apiUrl = '/todos/';

    async function fetchTodos() {
        const response = await fetch(apiUrl);
        const todos = await response.json();
        todoList.innerHTML = '';
        todos.forEach(todo => {
            const li = document.createElement('li');
            li.className = todo.completed ? 'completed' : '';
            li.innerHTML = `
                <span onclick="toggleComplete('${todo._id}', ${todo.completed})">${todo.name}: ${todo.description}</span>
                <button onclick="deleteTodo('${todo._id}')">Delete</button>
            `;
            todoList.appendChild(li);
        });
    }

    todoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = nameInput.value;
        const description = descriptionInput.value;
        await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, description, completed: false })
        });
        nameInput.value = '';
        descriptionInput.value = '';
        fetchTodos();
    });

    window.toggleComplete = async (id, completed) => {
        const response = await fetch(`${apiUrl}${id}`);
        const todo = await response.json();
        await fetch(`${apiUrl}${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ...todo, completed: !completed })
        });
        fetchTodos();
    };

    window.deleteTodo = async (id) => {
        await fetch(`${apiUrl}${id}`, {
            method: 'DELETE'
        });
        fetchTodos();
    };

    fetchTodos();
});
