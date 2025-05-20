Here's how you would set up your unit tests for the LoginForm component:

```jsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import LoginForm from './LoginForm';

describe('LoginForm', () => {
  it('renders correctly', () => {
    const { getByPlaceholderText } = render(<LoginForm handleLogin={jest.fn()} />);
    expect(getByPlaceholderText('Username')).toBeInTheDocument();
    expect(getByPlaceholderText('Password')).toBeInTheDocument();
  });

  it('calls handleLogin prop when form is submitted', () => {
    const handleLoginMock = jest.fn();
    const { getByPlaceholderText, getByText } = render(<LoginForm handleLogin={handleLoginMock} />);
    
    fireEvent.change(getByPlaceholderText('Username'), { target: { value: 'testuser' } });
    fireEvent.change(getByPlaceholderText('Password'), { target: { value: 'testpassword' } });
    fireEvent.click(getByText('Login'));
    
    expect(handleLoginMock).toHaveBeenCalledWith({ username: 'testuser', password: 'testpassword' });
  });

  it('does not call handleLogin prop when username and password are not provided', () => {
    const handleLoginMock = jest.fn();
    const { getByText } = render(<LoginForm handleLogin={handleLoginMock} />);
    
    fireEvent.click(getByText('Login'));
    
    expect(handleLoginMock).not.toHaveBeenCalled();
  });

  it('shows an alert when username and password are not provided', () => {
    const alertSpy = jest.spyOn(window, 'alert');
    const { getByText } = render(<LoginForm handleLogin={jest.fn()} />);
    
    fireEvent.click(getByText('Login'));
    
    expect(alertSpy).toHaveBeenCalledWith('Username and Password are required!');
  });
});
```
This test suite covers rendering of the LoginForm component, user interactions like typing in the username and password and clicking the Login button, and edge cases like submitting the form without username or password. It also ensures that the handleLogin function prop is called with the correct arguments when the form is submitted.

For props validation, React itself will warn you in the console if the handleLogin prop is not provided or if it's not a function, thanks to the PropTypes declaration in the LoginForm component. However, Jest can't catch these warnings. If you want to assert on them in your tests, you would need to use a package like `jest-prop-type-error` to turn these warnings into actual errors.