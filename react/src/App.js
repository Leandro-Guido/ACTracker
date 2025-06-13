import React, { useState, useRef } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import "./App.css";
import { FaFilm, FaUpload, FaChartBar } from "react-icons/fa"; // Importe ícones

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [actorStats, setActorStats] = useState({});
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");
  const [showResults, setShowResults] = useState(false);
  const analyzeButtonRef = useRef(null); // Criamos uma ref para o botão
  const [selectedOption1, setSelectedOption1] = useState("");
  const [selectedOption2, setSelectedOption2] = useState("");
  const [availableActors, setAvailableActors] = useState([]);
  const [showHelp, setShowHelp] = useState(false);

  // Opções para o primeiro dropdown (simuladas)
  const options1 = [
    "Um Sonho de Liberdade",
    "O Poderoso Chefão",
    "Batman: O Cavaleiro das Trevas",
    "O Poderoso Chefão: Parte II",
    "12 Homens e uma Sentença",
    "O Senhor dos Anéis: O Retorno do Rei",
    "A Lista de Schindler",
    "Pulp Fiction: Tempo de Violência",
    "O Senhor dos Anéis: A Sociedade do Anel",
    "Três Homens em Conflito",
  ];

  const handleOption1Change = (event) => {
    const value = event.target.value;
    setSelectedOption1(value);
    setSelectedOption2(""); // Resetar a segunda opção ao mudar a primeira
    fetchActorsForMovie(value); // Agora esta função busca atores
  };

  const handleOption2Change = (event) => {
    setSelectedOption2(event.target.value);
  };

  const handleFileUpload = async () => {
    if (!selectedOption1 || !selectedOption2) {
      // A nova condição de validação aqui
      setError(
        "Por favor, selecione um filme e um(a) ator/atriz para análise."
      );
      return;
    }

    setLoading(true);
    setProgress(0);
    setError("");
    setActorStats({});
    setShowResults(false);

    // Adiciona a classe para largura fixa ao clicar
    if (analyzeButtonRef.current) {
      analyzeButtonRef.current.classList.add("button-fixed-width");
    }

    // Simulação de um backend com barra de progresso
    const interval = setInterval(() => {
      setProgress((prevProgress) => {
        const newProgress = prevProgress + 10;
        if (newProgress >= 100) {
          clearInterval(interval);
          // Simulação dos resultados após o "upload"
          setTimeout(() => {
            const resultadosSimulados = {
              "": {
                cenas: 15,
                falas: 250,
                tempoTela: "25",
                tempoTelaNumerico: 25,
              },
            };
            setActorStats(resultadosSimulados);
            setLoading(false);
            setShowResults(true);
            // Remove a classe de largura fixa após o processamento
            if (analyzeButtonRef.current) {
              analyzeButtonRef.current.classList.remove("button-fixed-width");
            }
          }, 500);
          return 100;
        }
        return newProgress;
      });
    }, 200);

    // const analyzeData = async () => {
    //   // 1. Iniciar o estado de carregamento e progresso
    //   setLoading(true);
    //   setProgress(0); // O progresso será atualizado pelo backend ou deixado em 0 e só mostrar o spinner

    //   // Opcional: Se quiser uma barra de progresso real, você precisaria de um endpoint no backend que reportasse o progresso
    //   // Caso contrário, a barra de progresso pode apenas "girar" ou ir até 99% e finalizar ao receber a resposta.
    //   // Por simplicidade, vamos considerar que o progresso será atualizado apenas no início e no fim.
    //   // Se quiser um progresso que avança, você precisaria de WebSockets ou long-polling, o que é mais complexo.
    //   // Para a maioria dos casos de uso, um spinner ou barra de progresso indefinida é suficiente durante a requisição.

    //   try {
    //     // 2. Fazer a requisição à API
    //     // Substitua '/api/analisar-dados' pelo endpoint real da sua API
    //     // E 'corpoDaRequisicao' pelos dados que você precisa enviar (ex: um arquivo, texto, etc.)
    //     const response = await fetch('/api/analisar-dados', {
    //       method: 'POST', // Ou 'GET', 'PUT', dependendo da sua API
    //       headers: {
    //         'Content-Type': 'application/json',
    //         // Se precisar de autenticação, adicione aqui (ex: 'Authorization': `Bearer ${token}`)
    //       },
    //       body: JSON.stringify({ /* seus dados aqui */ }), // Se você estiver enviando dados no corpo da requisição
    //     });

    //     // 3. Lidar com a resposta da API
    //     if (!response.ok) {
    //       // Se a resposta não for bem-sucedida (ex: status 400, 500)
    //       const errorData = await response.json(); // Tenta ler o erro do corpo da resposta
    //       throw new Error(errorData.message || 'Erro ao processar a requisição.');
    //     }

    //     // 4. Converter a resposta para JSON
    //     const data = await response.json();

    //     // 5. Atualizar o estado com os resultados da API
    //     setProgress(100); // Marca o progresso como completo
    //     setActorStats(data.resultados); // Assumindo que a API retorna um objeto com 'resultados'
    //     setShowResults(true);

    //   } catch (error) {
    //     // 6. Lidar com erros na requisição
    //     console.error('Erro na requisição da API:', error);
    //     // Você pode definir um estado de erro para mostrar uma mensagem ao usuário
    //     // setErrorState(error.message);
    //     setProgress(0); // Reseta o progresso em caso de erro
    //     // Opcional: Reverter estados de carregamento se precisar
    //   } finally {
    //     // 7. Finalizar o estado de carregamento, independentemente do sucesso ou erro
    //     setLoading(false);
    //     // Remover a classe de largura fixa, se aplicável
    //     if (analyzeButtonRef.current) {
    //       analyzeButtonRef.current.classList.remove("button-fixed-width");
    //     }
    //   }
    // };

    // No seu projeto real, você faria algo semelhante para adicionar e remover a classe
    // ao iniciar e concluir a chamada da API.
  };

  const TMDB_BEARER_TOKEN =
    "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiMDAxZTdlNzI5ZmZjNWRhYzdiYmE5NTI0ZWQ2NDgxZSIsIm5iZiI6MTY1NTQ5NTk2My45MjEsInN1YiI6IjYyYWNkZDFiNWFiODFhMDA4YjgzY2Y3YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.KYEg81JxLA_ObhIezsOX9yBxzFRWm7eocp1asItmMTQ";

  const fetchActorsForMovie = async (movieTitle) => {
    if (!movieTitle) {
      setAvailableActors([]);
      setSelectedOption2(""); // Limpa a seleção do segundo dropdown
      return;
    }

    console.log(`Buscando filme e atores para: ${movieTitle}`);
    try {
      // 1. Pesquisar o filme pelo título
      const searchResponse = await fetch(
        `https://api.themoviedb.org/3/search/movie?query=${encodeURIComponent(
          movieTitle
        )}&language=pt-BR`,
        {
          headers: {
            Authorization: `Bearer ${TMDB_BEARER_TOKEN}`,
            "Content-Type": "application/json;charset=utf-8",
          },
        }
      );

      if (!searchResponse.ok) {
        throw new Error(`Erro na busca do filme: ${searchResponse.status}`);
      }
      const searchData = await searchResponse.json();

      if (searchData.results.length === 0) {
        setAvailableActors([]);
        setSelectedOption2("");
        setError("Nenhum filme encontrado com este título.");
        return;
      }

      // Pegar o ID do primeiro filme encontrado (geralmente o mais relevante)
      const movieId = searchData.results[0].id;
      console.log(`ID do filme encontrado: ${movieId}`);

      // 2. Buscar os créditos (atores) do filme usando o ID
      const creditsResponse = await fetch(
        `https://api.themoviedb.org/3/movie/${movieId}/credits?language=pt-BR`,
        {
          headers: {
            Authorization: `Bearer ${TMDB_BEARER_TOKEN}`,
            "Content-Type": "application/json;charset=utf-8",
          },
        }
      );

      if (!creditsResponse.ok) {
        throw new Error(
          `Erro ao buscar créditos do filme: ${creditsResponse.status}`
        );
      }
      const creditsData = await creditsResponse.json();

      // Extrair os nomes dos principais atores (e.g., os 5 primeiros ou os com 'order' baixo)
      const topActors = creditsData.cast
        .sort((a, b) => a.order - b.order) // Opcional: ordenar por 'order' para pegar os "principais"
        .slice(0, 10) // Pegar, por exemplo, os 10 primeiros atores
        .map((actor) => actor.name);

      setAvailableActors(topActors);
      setSelectedOption2(""); // Limpa a seleção anterior do segundo dropdown
      setError("");
    } catch (error) {
      console.error("Erro ao buscar filmes/atores na TMDB:", error);
      setError(
        "Erro ao carregar atores para o filme. Verifique o título ou sua conexão."
      );
      setAvailableActors([]);
      setSelectedOption2("");
    }
  };

  const toggleHelp = () => {
    setShowHelp(!showHelp);
  };

  const showAnalyzeButton = selectedOption1 && selectedOption2;

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>
          <FaFilm className="header-icon" /> ACTracker{" "}
        </h1>
        <p>Envie seu filme e descubra estatísticas detalhadas por ator!</p>
      </header>

      <main className="app-main">
        <div className="help-button-container">
          <button className="help-button" onClick={toggleHelp}>
            ?
          </button>
          {showHelp && <div className="help-message-box">A porcentagem referente ao tempo de tela do ator ou atriz escolhido(a) pode ser baixa, pois a análise é feita sobre todas as cenas do filme até mesmo cenas que não contêm atores.</div>}
        </div>
        <div className="dropdown-form-section">
          <div className="dropdown-group">
            <label htmlFor="dropdown1" className="dropdown-label">
              Selecione um opção:
            </label>
            <div className="custom-dropdown-wrapper">
              <select
                id="dropdown1"
                className="custom-dropdown"
                value={selectedOption1}
                onChange={handleOption1Change}
              >
                <option value="" disabled>
                  Escolha um filme:
                </option>
                {options1.map((option, index) => (
                  <option key={index} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {selectedOption1 && ( // O segundo dropdown só aparece se o primeiro for selecionado
            <div className="dropdown-group fade-in">
              <label htmlFor="dropdown2" className="dropdown-label">
                Selecione um(a) Ator/Atriz:
              </label>
              <div className="custom-dropdown-wrapper">
                <select
                  id="dropdown2"
                  className="custom-dropdown"
                  value={selectedOption2}
                  onChange={handleOption2Change}
                >
                  <option value="" disabled>
                    Escolha uma opção
                  </option>
                  {availableActors.map((option, index) => (
                    <option key={index} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          )}
        </div>
        <div className="upload-section">
          
          {showAnalyzeButton && (
            <>
              {loading && <p>A análise pode demorar alguns minutos</p>}
              <button
                onClick={handleFileUpload}
                disabled={loading}
                ref={analyzeButtonRef} // Atribuímos a ref ao botão
              >
                {loading ? (
                  <div className="progress-bar-container">
                    <div
                      className="progress-bar"
                      style={{ width: `${progress}%` }}
                    >
                      {progress}%
                    </div>
                  </div>
                ) : (
                  <>
                    <FaChartBar className="button-icon" /> Analisar Filme
                  </>
                )}
              </button>
            </>
          )}
          {error && <p className="error-message">{error}</p>}
        </div>

        {showResults && Object.keys(actorStats).length > 0 && (
          <div
            className={`results-section ${
              showResults ? "fade-in" : "fade-out"
            }`}
          >
            <h2>{selectedOption2}</h2>
            <ul className="actor-list">
              {Object.entries(actorStats).map(([ator, stats]) => (
                <li key={ator} className="actor-item">
                  <p>
                    <strong>Cenas:</strong> {stats.cenas}
                  </p>
                  <p>
                    <strong>Falas:</strong> {stats.falas}
                  </p>
                  <p>
                    <strong>Tempo de Tela:</strong> {stats.tempoTela} minutos
                  </p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>&copy; {new Date().getFullYear()} - ACTracker </p>
      </footer>
    </div>
  );
}

export default App;
