import React from 'react';
import { Link } from 'react-router-dom';
import Artist from './Artist';

const ArtistList = (props) => {

        if (props.artists.length) {
            return (

                <div className="ArtistList">
                    {props.artists.map(artist =>
                        <div key={artist.mbid}>
                            <Link to={'/artists/' + artist.mbid} >
                                <Artist artist={artist} selectArtist={props.selectArtist}/>
                            </Link>
                        </div>
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