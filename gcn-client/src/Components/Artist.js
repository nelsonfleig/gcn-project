import React from 'react';
// import './Artist.css';

const Artist = (props) => {

    /* On click go to artist page component */
    const renderAction = () => {
        // Render Artist page component with predictions
    }

    return (
        <div className="Artist" onClick={() => props.selectArtist(props.artist.mbid)}>
            <div className="Artist-information">
                <p>{props.artist.name} | {props.artist.country}</p>
            </div>
            {renderAction()}
        </div>
    );
}

export default Artist;
