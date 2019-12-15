import React from 'react';
// import './Artist.css';

const Artist = (props) => {

    /* On click go to artist page component */
    const renderAction = () => {
        // Render Artist page component with predictions
    }

    return (
        <div className="Artist">
            <div className="Artist-information">
                <p>{props.artist.ArtistName} | {props.artist.Country}</p>
            </div>
            {renderAction()}
        </div>
    );
}

export default Artist;
