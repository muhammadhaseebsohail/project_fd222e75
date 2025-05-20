Here's how you can create a login form component using React:

1. The complete component code with all imports:

```jsx
import React, { useState } from "react";
import PropTypes from 'prop-types';
import './LoginForm.css';

/**
 * LoginForm Component
 * @param {Object} props 
 * @param {Function} props.handleLogin Function to handle login
 */
const LoginForm = ({ handleLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if(username && password) {
      handleLogin({ username, password });
    } else {
      alert('Username and Password are required!');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="loginForm">
      <input 
        type="text" 
        value={username} 
        onChange={(e) => setUsername(e.target.value)} 
        placeholder="Username" 
        required
      />
      <input 
        type="password" 
        value={password} 
        onChange={(e) => setPassword(e.target.value)} 
        placeholder="Password" 
        required
      />
      <button type="submit">Login</button>
    </form>
  );
};

export default LoginForm;
```

2. Any necessary CSS/styling:

```css
/* LoginForm.css */
.loginForm {
  display: flex;
  flex-direction: column;
  width: 200px;
  margin: 0 auto;
}

.loginForm input {
  margin-bottom: 10px;
  padding: 5px;
}

.loginForm button {
  padding: 5px;
}
```

3. PropTypes:

```jsx
LoginForm.propTypes = {
  handleLogin: PropTypes.func.isRequired,
};
```

4. Export statements:

```jsx
export default LoginForm;
```

In this example, the LoginForm component accepts a prop `handleLogin` which is a function to be executed when the form is submitted. The component maintains its own state for the username and password and updates it as the user types in the respective input fields. The form is submitted only when both the username and password are provided, else an alert is shown to the user.