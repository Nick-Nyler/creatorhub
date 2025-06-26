import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';

const JobDetail = ({ user }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/api/v1/jobs/${id}`)
      .then(response => setJob(response.data))
      .catch(error => console.error(error));
  }, [id]);

  const formik = useFormik({
    initialValues: { cover_letter: '', price_offer: '' },
    validationSchema: Yup.object({
      cover_letter: Yup.string(),
      price_offer: Yup.number().required('Required').positive('Must be positive'),
    }),
    onSubmit: async (values) => {
      try {
        await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/applications`, { ...values, job_id: id });
        alert('Application submitted');
        navigate('/dashboard');
      } catch (error) {
        alert(error.response?.data?.error || 'Application failed');
      }
    },
  });

  const paymentFormik = useFormik({
    initialValues: { phone_number: '', amount: '' },
    validationSchema: Yup.object({
      phone_number: Yup.string().matches(/^\+?\d{10,12}$/, 'Invalid phone number').required('Required'),
      amount: Yup.number().required('Required').positive('Must be positive'),
    }),
    onSubmit: async (values) => {
      try {
        await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/payment`, { ...values, job_id: id, creator_id: job?.applications?.[0]?.creator_id });
        alert('Payment request sent to your phone!');
      } catch (error) {
        alert(error.response?.data?.error || 'Payment initiation failed');
      }
    },
  });

  if (!job) return <div>Loading...</div>;

  return (
    <div className="container">
      <div className="card">
        <h2>{job.title}</h2>
        <p>{job.description}</p>
        <p>Budget: ${job.budget}</p>
        <p>Deadline: {new Date(job.deadline).toLocaleDateString()}</p>
        {user?.role === 'creator' && (
          <form onSubmit={formik.handleSubmit} style={{ marginTop: '20px' }}>
            <div className="form-group">
              <label>Cover Letter</label>
              <textarea
                name="cover_letter"
                {...formik.getFieldProps('cover_letter')}
              />
            </div>
            <div className="form-group">
              <label>Price Offer</label>
              <input
                type="number"
                name="price_offer"
                {...formik.getFieldProps('price_offer')}
              />
              {formik.touched.price_offer && formik.errors.price_offer && (
                <p className="error">{formik.errors.price_offer}</p>
              )}
            </div>
            <button type="submit" className="btn btn-primary">Apply</button>
          </form>
        )}
        {user?.role === 'client' && job.client_id === user.id && (
          <form onSubmit={paymentFormik.handleSubmit} style={{ marginTop: '20px' }}>
            <div className="form-group">
              <label>Phone Number</label>
              <input
                type="text"
                name="phone_number"
                {...paymentFormik.getFieldProps('phone_number')}
              />
              {paymentFormik.touched.phone_number && paymentFormik.errors.phone_number && (
                <p className="error">{paymentFormik.errors.phone_number}</p>
              )}
            </div>
            <div className="form-group">
              <label>Amount</label>
              <input
                type="number"
                name="amount"
                {...paymentFormik.getFieldProps('amount')}
              />
              {paymentFormik.touched.amount && paymentFormik.errors.amount && (
                <p className="error">{paymentFormik.errors.amount}</p>
              )}
            </div>
            <button type="submit" className="btn btn-success">Pay Creator</button>
          </form>
        )}
      </div>
    </div>
  );
};

export default JobDetail;