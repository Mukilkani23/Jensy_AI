import { useState, useEffect } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import './Planner.css';

import { enUS } from 'date-fns/locale';

const locales = {
  'en-US': enUS,
};


const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

export default function Planner() {
  const { token } = useAuth();
  const [events, setEvents] = useState([]);
  const [examDate, setExamDate] = useState('');
  const [subjects, setSubjects] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchPlan();
  }, []);

  const fetchPlan = async () => {
    try {
      const res = await axios.get('http://localhost:8000/planner/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.data.events) {
        const formattedEvents = res.data.events.map(ev => ({
          ...ev,
          start: new Date(ev.start),
          end: new Date(ev.end)
        }));
        setEvents(formattedEvents);
      }
    } catch (err) {
      console.error("Failed to fetch plan", err);
    }
  };

  const generatePlan = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const subjectArray = subjects.split(',').map(s => s.trim());
      const res = await axios.post('http://localhost:8000/planner/generate', {
        exam_date: new Date(examDate).toISOString(),
        subjects: subjectArray
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      const formattedEvents = res.data.events.map(ev => ({
        ...ev,
        start: new Date(ev.start),
        end: new Date(ev.end)
      }));
      setEvents(formattedEvents);
    } catch (err) {
      console.error("Failed to generate plan", err);
      alert("Failed to generate plan. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const eventStyleGetter = (event) => {
    return {
      style: {
        backgroundColor: event.color || '#3b82f6',
        borderRadius: '5px',
        opacity: 0.8,
        color: 'white',
        border: '0px',
        display: 'block'
      }
    };
  };

  return (
    <div className="planner-container">
      <div className="planner-header">
        <h1>AI Study Planner</h1>
        <p>Generate a customized study schedule leading up to your exams.</p>
      </div>

      <div className="planner-controls glass-panel">
        <form onSubmit={generatePlan}>
          <div className="form-group">
            <label>Exam Date</label>
            <input 
              type="date" 
              value={examDate} 
              onChange={(e) => setExamDate(e.target.value)} 
              required 
            />
          </div>
          <div className="form-group">
            <label>Subjects (comma separated codes)</label>
            <input 
              type="text" 
              placeholder="CS101, MA201, PH301" 
              value={subjects} 
              onChange={(e) => setSubjects(e.target.value)} 
              required 
            />
          </div>
          <button type="submit" disabled={loading} className="generate-btn">
            {loading ? "Generating..." : "Generate AI Plan"}
          </button>
        </form>
      </div>

      <div className="calendar-container glass-panel">
        <Calendar
          localizer={localizer}
          events={events}
          startAccessor="start"
          endAccessor="end"
          style={{ height: 600 }}
          eventPropGetter={eventStyleGetter}
          views={['month', 'week', 'day']}
        />
      </div>
    </div>
  );
}
