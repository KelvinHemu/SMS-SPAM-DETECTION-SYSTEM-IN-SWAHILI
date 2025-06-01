import React from 'react';

const ScenarioSelector = ({ selectedScenario, onScenarioChange, phoneScenarios }) => (
  <div className="w-[280px] bg-blue-50 rounded-xl p-4 shadow-md">
    <label className="block text-sm font-medium text-blue-800 mb-2">
      Select Test Scenario:
    </label>
    <select 
      value={selectedScenario}
      onChange={(e) => onScenarioChange(e.target.value)}
      className="w-full text-sm px-3 py-2 border border-blue-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
    >
      <optgroup label="✅ Verified Numbers">
        {Object.entries(phoneScenarios)
          .filter(([key, scenario]) => scenario.category === 'verified')
          .map(([key, scenario]) => (
            <option key={key} value={key}>
              {scenario.label}
            </option>
          ))}
      </optgroup>
      <optgroup label="🚨 Flagged Numbers">
        {Object.entries(phoneScenarios)
          .filter(([key, scenario]) => scenario.category === 'flagged')
          .map(([key, scenario]) => (
            <option key={key} value={key}>
              {scenario.label}
            </option>
          ))}
      </optgroup>
    </select>
    <div className="text-sm text-blue-600 mt-2">
      💡 Same message, different results based on sender reputation!
    </div>
  </div>
);

export default ScenarioSelector; 