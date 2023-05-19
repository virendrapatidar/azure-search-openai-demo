import { Example } from "./Example";

import styles from "./Example.module.css";

export type ExampleModel = {
    text: string;
    value: string;
};

const EXAMPLES: ExampleModel[] = [
    // {
    //     text: "How to login into Sasai super App?",
    //     value: "How to login into Sasai super App?"
    // },
    { text: "I want to send money", value: "I want to send money" },
    { text: "What are features supported in micro loan?", value: "What are features supported in micro loan?" },
    { text: "What are capabilities of Sasai Payment Gateway?", value: "What are capabilities of Sasai Payment Gateway?" }
];

interface Props {
    onExampleClicked: (value: string) => void;
}

export const ExampleList = ({ onExampleClicked }: Props) => {
    return (
        <ul className={styles.examplesNavList}>
            {EXAMPLES.map((x, i) => (
                <li key={i}>
                    <Example text={x.text} value={x.value} onClick={onExampleClicked} />
                </li>
            ))}
        </ul>
    );
};
