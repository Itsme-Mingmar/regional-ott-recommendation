# Regional OTT Video Recommender

A content-based video recommendation system for the Regional OTT platform, converted from Jupyter notebook to a production-ready Python application.

## Project Structure

```
regional-ott-recommendation/
├── model/
│   ├── recommender.py      # Core recommendation logic
│   ├── similarity.pkl      # Pre-computed similarity matrix
│   ├── movies.pkl          # Processed video data
│   └── vectorizer.pkl      # Trained text vectorizer
├── app.py                  # Flask API server
├── build_model.py          # Script to train the model
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Features

- **Content-based recommendations**: Recommends videos based on description, genre, language, category, and province
- **User preference recommendations**: Suggests videos based on user's liked videos
- **Province-based filtering**: Get popular videos from specific provinces
- **RESTful API**: Easy integration with your OTT platform
- **Model persistence**: Save and load trained models

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download NLTK data:**
   ```python
   import nltk
   nltk.download('punkt')
   ```

## Usage

### 1. Export Your Video Data

First, export your video data from your backend database:

```bash
# Option 1: Export from your API
python export_data.py http://localhost:5000/api/videos

# Option 2: Create sample data for testing
python export_data.py
```

This creates `data/videos.csv` with your video data in the correct format.

### 2. Build the Model

```bash
python build_model.py
```

This will:
- Load your video data from `data/videos.csv`
- Preprocess the text
- Build the recommendation model
- Save the model files to `model/`

### 3. Run the API Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Get Recommendations for a Video
```
GET /recommend/<title>
```
Example: `GET /recommend/Movie%201`

### Get Recommendations for User
```
POST /recommend/user
Content-Type: application/json

{
  "preferences": ["Movie 1", "Movie 2"],
  "top_n": 5
}
```

### Get Video Details
```
GET /video/<title>
```

### Get Popular Videos by Province
```
GET /popular/<province>
```

### Load Saved Model
```
GET /load-model
```

### Build New Model
```
GET /build-model
```

## Integration with Your OTT Platform

### Backend Integration

You can integrate this recommender with your Node.js backend by making HTTP requests to the Flask API:

```javascript
// In your video controller
const axios = require('axios');

const getRecommendations = async (videoTitle) => {
  try {
    const response = await axios.get(`http://localhost:5000/recommend/${encodeURIComponent(videoTitle)}`);
    return response.data.recommendations;
  } catch (error) {
    console.error('Error getting recommendations:', error);
    return [];
  }
};
```

### Frontend Integration

Add recommendation components to your React frontend:

```jsx
// In your VideoDetailsPage.jsx
import { useEffect, useState } from 'react';

const VideoDetailsPage = ({ videoTitle }) => {
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    fetch(`/api/recommendations/${encodeURIComponent(videoTitle)}`)
      .then(res => res.json())
      .then(data => setRecommendations(data.recommendations));
  }, [videoTitle]);

  return (
    <div>
      <h2>Recommended Videos</h2>
      {recommendations.map(rec => (
        <div key={rec.id}>
          <h3>{rec.title}</h3>
          <p>Genre: {rec.genre} | Province: {rec.province}</p>
        </div>
      ))}
    </div>
  );
};
```

## Model Details

The recommender uses:
- **Text preprocessing**: Tokenization, stemming, stop word removal
- **Feature extraction**: CountVectorizer with 5000 max features
- **Similarity calculation**: Cosine similarity between video feature vectors
- **Recommendation algorithm**: Content-based filtering

## Customization

### Adding More Features

Edit `recommender.py` to include additional video features:

```python
# Add more features to tags
self.movies_df['tags'] = (
    self.movies_df['description'] +
    self.movies_df['genre'] +
    self.movies_df['language'] +
    self.movies_df['category'] +
    self.movies_df['province'] +
    self.movies_df['director'] +  # Add director
    self.movies_df['cast']        # Add cast
)
```

### Database Integration

Replace the data loading in `build_model.py`:

```python
def load_video_data_from_database():
    # Connect to your MongoDB
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ott_platform']
    videos = list(db.videos.find({}))

    # Convert to DataFrame
    df = pd.DataFrame(videos)
    return df
```

## Troubleshooting

### Model Not Found
If you get "Model not found" error:
1. Run `python build_model.py` to train the model
2. Check that `model/` directory exists with `.pkl` files

### No Recommendations
- Ensure video titles match exactly (case-sensitive)
- Check that the model was trained with your data
- Verify CSV format if using file-based data

### Memory Issues
For large datasets:
- Reduce `max_features` in CountVectorizer
- Use sparse matrices for similarity calculation
- Implement batch processing for large datasets

## Future Enhancements

- **Collaborative filtering**: Add user-based recommendations
- **Hybrid approach**: Combine content-based and collaborative filtering
- **Real-time updates**: Update model as new videos are added
- **A/B testing**: Compare different recommendation algorithms
- **Personalization**: Include user watch history and preferences