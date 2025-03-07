import { useEffect, useState } from 'react';
import TypingEffect from '../components/TypingEffect';

export default function Home() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    fetch('http://localhost:8000/items/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setItems(data.items))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:8000/items/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, description }),
    });
    if (response.ok) {
      const newItem = await response.json();
      setItems([...items, newItem]);
    }
  };

  return (
    <div>
      <TypingEffect />
      <div>
        <ul>
          {items.map(item => (
            <li key={item.id}>
              <h2>{item.name}</h2>
              <p>{item.description}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
