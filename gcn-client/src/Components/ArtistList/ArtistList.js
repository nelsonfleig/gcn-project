import React from 'react';
// import './ArtistList.css';
import Artist from '../Artist/Artist'

const ArtistList = (props) => {
    if (props.artists.length) {
        return (
            <div className="ArtistList">
                {props.artists.map(artist =>
                    <Artist artist={artist} key={artist.mbid} />
                )}
            </div>
        )
    } else {
        return (
            <div className="ArtistList">

            </div>
        )
    }
}
export default ArtistList;