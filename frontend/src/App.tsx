import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Signup from './pages/Signup';
import Login from './pages/Login';

const Home = () => (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
        <h1 className="text-4xl font-bold text-gray-900">Welcome to Staboost</h1>
        <p className="mt-2 text-lg text-gray-600">Your one-stop solution for social media marketing.</p>
        <div className="mt-8 space-x-4">
            <Link to="/login" className="px-4 py-2 font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700">
                Log In
            </Link>
            <Link to="/signup" className="px-4 py-2 font-medium text-indigo-700 bg-indigo-100 rounded-md hover:bg-indigo-200">
                Sign Up
            </Link>
        </div>
    </div>
);

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/login" element={<Login />} />
            </Routes>
        </Router>
    );
}

export default App;
