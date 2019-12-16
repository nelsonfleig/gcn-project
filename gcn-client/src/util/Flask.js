const Flask = {
    getArtists: () => {
        return fetch('http://127.0.0.1:5000/')
          .then(response => response.json())
          .then(jsonResponse => {
            if (jsonResponse) {
              return jsonResponse.map(artist => {
                return {
                    mbid: artist.mbid,
                    name: artist.name,
                    country: artist.country
                }
              })
            } else {
                return {}
            }
          })
    }
}

export default Flask;