import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';

const PortfolioUploader = ({ user }) => {
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: { title: '', description: '', image_url: '' },
    validationSchema: Yup.object({
      title: Yup.string().required('Required'),
      description: Yup.string(),
      image_url: Yup.string().url('Invalid URL'),
    }),
    onSubmit: async (values) => {
      try {
        await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/portfolio`, values);
        alert('Portfolio item added');
        navigate('/dashboard');
      } catch (error) {
        alert(error.response?.data?.error || 'Failed to add portfolio item');
      }
    },
  });

  if (user?.role !== 'creator') return <div>Unauthorized</div>;

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: '400px', margin: '40px auto' }}>
        <h2>Upload Portfolio Item</h2>
        <form onSubmit={formik.handleSubmit}>
          <div className="form-group">
            <label>Title</label>
            <input
              type="text"
              name="title"
              {...formik.getFieldProps('title')}
            />
            {formik.touched.title && formik.errors.title && (
              <p className="error">{formik.errors.title}</p>
            )}
          </div>
          <div className="form-group">
            <label>Description</label>
            <textarea
              name="description"
              {...formik.getFieldProps('description')}
            />
          </div>
          <div className="form-group">
            <label>Image URL</label>
            <input
              type="text"
              name="image_url"
              {...formik.getFieldProps('image_url')}
            />
            {formik.touched.image_url && formik.errors.image_url && (
              <p className="error">{formik.errors.image_url}</p>
            )}
          </div>
          <button type="submit" className="btn btn-primary">Upload</button>
        </form>
      </div>
    </div>
  );
};

export default PortfolioUploader;