const Flask = {
    getArtists: () => {
        return fetch('http://127.0.0.1:5000/')
          .then(response => response.json())
          .then(jsonResponse => {
            if (jsonResponse) {
              return jsonResponse.map(artist => {
                return {
                    id: artist.id,
                    ArtistName: artist.ArtistName,
                    Country: artist.Country
    
                }
              })
            } else {
                return {}
            }
          })
    }
}

export default Flask;