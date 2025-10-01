// Fetch and display users
document.addEventListener('DOMContentLoaded', function() {
    fetchUsers();
});

function fetchUsers() {
    fetch('/api/users')
        .then(response => response.json())
        .then(users => {
            const usersList = document.getElementById('users-list');
            if (users.length === 0) {
                usersList.innerHTML = '<p>No users found.</p>';
            } else {
                usersList.innerHTML = users.map(user => `
                    <div class="user-item">
                        <strong>${user.username}</strong> - ${user.email}
                    </div>
                `).join('');
            }
        })
        .catch(error => {
            console.error('Error fetching users:', error);
            document.getElementById('users-list').innerHTML = '<p>Error loading users.</p>';
        });
}
