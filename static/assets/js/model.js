const predict = async (lat, lng) => {
    return (await fetch(`/predict?lat=${lat}&lng=${lng}`)).json();
}