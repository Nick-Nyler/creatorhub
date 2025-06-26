import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';

const SignupForm = ({ setUser }) => {
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: { name: '', email: '', password: '', role: 'creator' },
    validationSchema: Yup.object({
      name: Yup.string().required('Required'),
      email: Yup.string().email('Invalid email').required('Required'),
      password: Yup.string().min(6, 'At least 6 characters').required('Required'),
      role: Yup.string().oneOf(['creator', 'client']).required('Required'),
    }),
    onSubmit: async (values) => {
      try {
        const response = await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/signup`, values);
        localStorage.setItem('token', response.data.access_token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
        setUser(response.data.user);
        navigate('/dashboard');
      } catch (error) {
        alert(error.response?.data?.error || 'Signup failed');
      }
    },
  });

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: '400px', margin: '40px auto' }}>
        <h2>Signup</h2>
        <form onSubmit={formik.handleSubmit}>
          <div className="form-group">
            <label>Name</label>
            <input
              type="text"
              name="name"
              {...formik.getFieldProps('name')}
            />
            {formik.touched.name && formik.errors.name && (
              <p className="error">{formik.errors.name}</p>
            )}
          </div>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              {...formik.getFieldProps('email')}
            />
            {formik.touched.email && formik.errors.email && (
              <p className="error">{formik.errors.email}</p>
            )}
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              {...formik.getFieldProps('password')}
            />
            {formik.touched.password && formik.errors.password && (
              <p className="error">{formik.errors.password}</p>
            )}
          </div>
          <div className="form-group">
            <label>Role</label>
            <select
              name="role"
              {...formik.getFieldProps('role')}
            >
              <option value="creator">Creator</option>
              <option value="client">Client</option>
            </select>
          </div>
          <button type="submit" className="btn btn-primary">Signup</button>
        </form>
      </div>
    </div>
  );
};

export default SignupForm;