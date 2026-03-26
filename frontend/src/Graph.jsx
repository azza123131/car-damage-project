import resultsImg from './assets/graphs/results.jpg';
import confusionImg from './assets/graphs/confusion_matrix.jpg';

function Graphs() {
  return (
    <div className="graphs-page">
      <h1>Model Training Graphs</h1>
      <div style={{ display: "flex", flexDirection: "column", gap: "30px" }}>
        <div>
          <h3>Training Results</h3>
          <img src={resultsImg} alt="Training Results" style={{ width: "600px" }} />
        </div>

        <div>
          <h3>Confusion Matrix</h3>
          <img src={confusionImg} alt="Confusion Matrix" style={{ width: "600px" }} />
        </div>

      </div>
    </div>
  );
}

export default Graphs;