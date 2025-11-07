import ReactMarkdown from 'react-markdown';

const MarkDownDisplay: React.FC<{ markdown: string }> = ({ markdown }) => {
    return (
        <div className="bg-white rounded-lg shadow-xl p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center border-b pb-2 border-gray-300">Analysis</h2>
            <ReactMarkdown
                components={{
                    h1: ({node, ...props}) =><h1 className="text-2xl text-purple-500 font-bold my-6" {...props}></h1>,
                    h2: ({node, ...props}) =><h2 className="text-xl text-purple-500 font-bold my-4" {...props}></h2>,
                    h3: ({node, ...props}) =><h3 className="text-lg text-purple-500 font-bold my-3" {...props}></h3>,
                    p: ({node, ...props}) =><p className="my-2 leading-7 text-gray-800" {...props}></p>,
                    li: ({node, ...props}) =><li className="list-disc list-inside my-1" {...props}></li>,
                    strong: ({node, ...props}) =><strong className="text-purple-500" {...props}></strong>,
                }}
            >
            {markdown}
            </ReactMarkdown>
        </div>
    );
};

export default MarkDownDisplay;