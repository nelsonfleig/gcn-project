import React from 'react';
import { Link } from 'react-router-dom';
import Artist from './Artist';
import SearchBar from './SearchBar';

const ArtistList = (props) => {

    if (props.searchResults.length) {
        return (
            <div>
                <SearchBar searchArtists={props.searchArtists} clearSearch={props.clearSearch} />
                <div className="ArtistList">
                    <h4 className="ArtistListTitle">Your search results:</h4>
                    {props.searchResults.map(artist =>
                        <div key={artist.mbid}>
                            <Link to={'/artists/' + artist.mbid} >
                                <Artist artist={artist} selectArtist={props.selectArtist}/>
                            </Link>
                        </div>
                    )}
                </div>
            </div>

        )
    }

    if (props.artists.length) {
        return (
            <div className="Artist">
                <SearchBar searchArtists={props.searchArtists} />
                <div className="ArtistList">
                    <h4 className="ArtistListTitle">Top Artists by Collaboration</h4>
                    {props.artists.map(artist =>
                        <div key={artist.mbid}>
                            <Link to={'/artists/' + artist.mbid} >
                                <Artist artist={artist} selectArtist={props.selectArtist}/>
                            </Link>
                        </div>
                    )}
                </div>
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