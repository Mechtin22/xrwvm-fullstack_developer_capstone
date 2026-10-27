const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');

const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

// Load JSON data
const reviews_data = JSON.parse(
    fs.readFileSync('reviews.json', 'utf8')
);

const dealerships_data = JSON.parse(
    fs.readFileSync('dealerships.json', 'utf8')
);

// Connect to MongoDB
mongoose.connect('mongodb://mongo_db:27017/', {
    dbName: 'dealershipsDB'
});

// Import Mongoose models
const Reviews = require('./review');
const Dealerships = require('./dealership');

// Populate MongoDB with the supplied JSON data
async function populateDatabase() {
    try {
        await mongoose.connection.asPromise();

        await Reviews.deleteMany({});
        await Reviews.insertMany(reviews_data.reviews);

        await Dealerships.deleteMany({});
        await Dealerships.insertMany(dealerships_data.dealerships);

        console.log('Reviews and dealerships populated successfully');
    } catch (error) {
        console.error('Error populating database:', error);
    }
}

mongoose.connection.once('open', () => {
    populateDatabase();
});

mongoose.connection.on('error', (error) => {
    console.error('MongoDB connection error:', error);
});

// Express route to home
app.get('/', async (req, res) => {
    res.send('Welcome to the Mongoose API');
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
    try {
        const documents = await Reviews.find();
        res.json(documents);
    } catch (error) {
        console.error(error);
        res.status(500).json({
            error: 'Error fetching documents'
        });
    }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
    try {
        const documents = await Reviews.find({
            dealership: Number(req.params.id)
        });

        res.json(documents);
    } catch (error) {
        console.error(error);
        res.status(500).json({
            error: 'Error fetching documents'
        });
    }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
    try {
        const documents = await Dealerships.find();
        res.json(documents);
    } catch (error) {
        console.error(error);
        res.status(500).json({
            error: 'Error fetching dealerships'
        });
    }
});

// Express route to fetch dealerships by state
app.get('/fetchDealers/:state', async (req, res) => {
    try {
        const documents = await Dealerships.find({
            state: req.params.state
        });

        res.json(documents);
    } catch (error) {
        console.error(error);
        res.status(500).json({
            error: 'Error fetching dealerships by state'
        });
    }
});

// Express route to fetch a dealership by ID
app.get('/fetchDealer/:id', async (req, res) => {
    try {
        const dealerId = Number(req.params.id);

        if (!Number.isFinite(dealerId)) {
            return res.status(400).json({
                error: 'Invalid dealership ID'
            });
        }

        const documents = await Dealerships.find({
            id: dealerId
        });

        res.json(documents);
    } catch (error) {
        console.error(error);
        res.status(500).json({
            error: 'Error fetching dealership by ID'
        });
    }
});

// Express route to insert a review
app.post(
    '/insert_review',
    express.raw({ type: '*/*' }),
    async (req, res) => {
        try {
            const data = JSON.parse(req.body.toString());

            // Find the highest existing review ID
            const latestReview = await Reviews.findOne().sort({
                id: -1
            });

            const newId = latestReview
                ? Number(latestReview.id) + 1
                : 1;

            const review = new Reviews({
                id: newId,
                name: data.name,
                dealership: data.dealership,
                review: data.review,
                purchase: data.purchase,
                purchase_date: data.purchase_date,
                car_make: data.car_make,
                car_model: data.car_model,
                car_year: data.car_year
            });

            const savedReview = await review.save();

            res.json(savedReview);
        } catch (error) {
            console.error('Error inserting review:', error);

            res.status(500).json({
                error: 'Error inserting review'
            });
        }
    }
);

// Start the Express server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});